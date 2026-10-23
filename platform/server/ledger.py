import sqlite3
import hashlib
import hmac
import secrets
import time
from typing import Optional, Dict, Any, List, Tuple
from contextlib import contextmanager

DB_PATH = "platform_core.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'player', -- 'player', 'admin'
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            balance REAL NOT NULL DEFAULT 0.0 CHECK (balance >= 0.0),
            updated_at REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS ledger_transactions (
            id TEXT PRIMARY KEY, -- UUID or custom tx hash
            user_id INTEGER NOT NULL,
            tx_type TEXT NOT NULL, -- 'DEPOSIT', 'WITHDRAWAL', 'BET', 'WIN', 'ROLLBACK'
            reference_id TEXT,    -- external game round ID or payment ref
            description TEXT,
            created_at REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS ledger_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            direction TEXT NOT NULL, -- 'DEBIT' (decrease), 'CREDIT' (increase)
            amount REAL NOT NULL CHECK (amount > 0.0),
            balance_after REAL NOT NULL,
            created_at REAL NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES ledger_transactions (id)
        );

        CREATE TABLE IF NOT EXISTS game_sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            game_id TEXT NOT NULL,
            expires_at REAL NOT NULL,
            used_at REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS payment_orders (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'COMPLETED', 'FAILED'
            provider TEXT NOT NULL,
            created_at REAL NOT NULL,
            completed_at REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """)

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def create_user(username: str, password: str, role: str = 'player', initial_balance: float = 100.0) -> Dict[str, Any]:
    pwd_hash, salt = hash_password(password)
    now = time.time()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE")
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, pwd_hash, salt, role, now)
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO wallets (user_id, currency, balance, updated_at) VALUES (?, 'USD', ?, ?)",
                (user_id, initial_balance, now)
            )
            if initial_balance > 0:
                tx_id = f"tx_init_{secrets.token_hex(8)}"
                cursor.execute(
                    "INSERT INTO ledger_transactions (id, user_id, tx_type, reference_id, description, created_at) VALUES (?, ?, 'DEPOSIT', 'SIGNUP_BONUS', 'Initial player bankroll', ?)",
                    (tx_id, user_id, now)
                )
                cursor.execute(
                    "INSERT INTO ledger_entries (transaction_id, user_id, direction, amount, balance_after, created_at) VALUES (?, ?, 'CREDIT', ?, ?, ?)",
                    (tx_id, user_id, initial_balance, initial_balance, now)
                )
            cursor.execute("COMMIT")
            return {"id": user_id, "username": username, "role": role, "balance": initial_balance}
        except Exception as e:
            cursor.execute("ROLLBACK")
            raise e

def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, salt, role FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
        user_id, uname, pwd_hash, salt, role = row
        calc_hash, _ = hash_password(password, salt)
        if secrets.compare_digest(pwd_hash, calc_hash):
            cursor.execute("SELECT balance, currency FROM wallets WHERE user_id = ?", (user_id,))
            w_row = cursor.fetchone()
            balance = w_row[0] if w_row else 0.0
            currency = w_row[1] if w_row else 'USD'
            return {"id": user_id, "username": uname, "role": role, "balance": balance, "currency": currency}
        return None

def get_wallet(user_id: int) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance, currency FROM wallets WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Wallet not found")
        return {"user_id": user_id, "balance": row[0], "currency": row[1]}

def execute_ledger_transaction(user_id: int, tx_type: str, direction: str, amount: float, reference_id: Optional[str] = None, description: str = "") -> Dict[str, Any]:
    """
    Guarantees strict double-entry ledger bookkeeping.
    direction: 'DEBIT' (decreases balance) or 'CREDIT' (increases balance).
    """
    if amount <= 0:
        raise ValueError("Transaction amount must be strictly positive")
    
    now = time.time()
    tx_id = f"tx_{secrets.token_hex(10)}"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE")
        try:
            cursor.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Wallet does not exist")
            
            current_balance = row[0]
            if direction == "DEBIT":
                if current_balance < amount:
                    raise ValueError(f"Insufficient funds: available {current_balance:.2f}, required {amount:.2f}")
                new_balance = round(current_balance - amount, 2)
            elif direction == "CREDIT":
                new_balance = round(current_balance + amount, 2)
            else:
                raise ValueError(f"Invalid direction: {direction}")

            cursor.execute("UPDATE wallets SET balance = ?, updated_at = ? WHERE user_id = ?", (new_balance, now, user_id))
            cursor.execute(
                "INSERT INTO ledger_transactions (id, user_id, tx_type, reference_id, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (tx_id, user_id, tx_type, reference_id, description, now)
            )
            cursor.execute(
                "INSERT INTO ledger_entries (transaction_id, user_id, direction, amount, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (tx_id, user_id, direction, amount, new_balance, now)
            )
            cursor.execute("COMMIT")
            return {
                "transaction_id": tx_id,
                "user_id": user_id,
                "type": tx_type,
                "direction": direction,
                "amount": amount,
                "balance_after": new_balance,
                "created_at": now
            }
        except Exception as e:
            cursor.execute("ROLLBACK")
            raise e
