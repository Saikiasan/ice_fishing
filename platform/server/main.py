import secrets
import time
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import ledger

ledger.init_db()

# Seed default admin and player if not present
try:
    ledger.create_user("admin", "admin123", role="admin", initial_balance=5000.0)
    ledger.create_user("player1", "player123", role="player", initial_balance=500.0)
    print("[INIT] Created demo users 'admin' and 'player1'")
except Exception:
    pass

app = FastAPI(title="Game Platform Core & Cashier API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session token store (maps token -> user dict)
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}
GAME_LAUNCH_TOKENS: Dict[str, Dict[str, Any]] = {}

# --- Models ---
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6)
    initial_deposit: float = Field(default=100.0, ge=0.0)

class LoginRequest(BaseModel):
    username: str
    password: str

class BetRequest(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0.0)
    round_id: str
    game_id: str = "ice_fishing"

class SettleWinRequest(BaseModel):
    user_id: int
    payout: float = Field(..., ge=0.0)
    round_id: str
    game_id: str = "ice_fishing"

class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0.0)
    payment_method: str = "local_fiat_instant"

class WithdrawRequest(BaseModel):
    amount: float = Field(..., gt=0.0)
    payout_details: str

# --- Auth Helper ---
def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.replace("Bearer ", "").strip()
    user = ACTIVE_SESSIONS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session token")
    # Fresh balance check
    wallet = ledger.get_wallet(user["id"])
    user["balance"] = wallet["balance"]
    return user

# --- Routes ---

@app.post("/api/v1/auth/register")
def register(req: RegisterRequest):
    try:
        user = ledger.create_user(req.username, req.password, role="player", initial_balance=req.initial_deposit)
        token = secrets.token_hex(24)
        ACTIVE_SESSIONS[token] = user
        return {"status": "ok", "token": token, "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/auth/login")
def login(req: LoginRequest):
    user = ledger.verify_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = secrets.token_hex(24)
    ACTIVE_SESSIONS[token] = user
    return {"status": "ok", "token": token, "user": user}

@app.get("/api/v1/auth/me")
def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return {"user": user}

@app.get("/api/v1/wallet/balance")
def get_balance(user: Dict[str, Any] = Depends(get_current_user)):
    wallet = ledger.get_wallet(user["id"])
    return {"user_id": user["id"], "balance": wallet["balance"], "currency": wallet["currency"]}

@app.post("/api/v1/cashier/deposit")
def deposit(req: DepositRequest, user: Dict[str, Any] = Depends(get_current_user)):
    tx = ledger.execute_ledger_transaction(
        user_id=user["id"],
        tx_type="DEPOSIT",
        direction="CREDIT",
        amount=req.amount,
        reference_id=f"order_{secrets.token_hex(6)}",
        description=f"Fiat deposit via {req.payment_method}"
    )
    return {"status": "completed", "transaction": tx}

@app.post("/api/v1/cashier/withdraw")
def withdraw(req: WithdrawRequest, user: Dict[str, Any] = Depends(get_current_user)):
    try:
        tx = ledger.execute_ledger_transaction(
            user_id=user["id"],
            tx_type="WITHDRAWAL",
            direction="DEBIT",
            amount=req.amount,
            reference_id=f"payout_{secrets.token_hex(6)}",
            description=f"Withdrawal request to: {req.payout_details}"
        )
        return {"status": "completed", "transaction": tx}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- RGS Internal Seamless Wallet Endpoints ---

@app.post("/api/v1/rgs/launch")
def create_game_launch_token(request: Request, game_id: str = "ice_fishing", user: Dict[str, Any] = Depends(get_current_user)):
    launch_token = f"gt_{secrets.token_hex(16)}"
    GAME_LAUNCH_TOKENS[launch_token] = {
        "user_id": user["id"],
        "username": user["username"],
        "game_id": game_id,
        "created_at": time.time(),
        "expires_at": time.time() + 300 # 5 min TTL
    }
    client_host = request.headers.get("host", "localhost:8000").split(":")[0]
    return {
        "launch_token": launch_token,
        "game_id": game_id,
        "ws_url": f"ws://{client_host}:8001/ws/{game_id}?token={launch_token}"
    }

@app.post("/api/v1/rgs/verify_token")
def verify_launch_token(token: str):
    data = GAME_LAUNCH_TOKENS.get(token)
    if not data or time.time() > data["expires_at"]:
        raise HTTPException(status_code=403, detail="Game session token expired or invalid")
    wallet = ledger.get_wallet(data["user_id"])
    return {
        "valid": True,
        "user_id": data["user_id"],
        "username": data["username"],
        "balance": wallet["balance"],
        "currency": wallet["currency"]
    }

@app.post("/api/v1/rgs/debit")
def rgs_debit(req: BetRequest):
    """Called by RGS to securely place a bet in the ledger."""
    try:
        tx = ledger.execute_ledger_transaction(
            user_id=req.user_id,
            tx_type="BET",
            direction="DEBIT",
            amount=req.amount,
            reference_id=req.round_id,
            description=f"Wager on {req.game_id} round {req.round_id}"
        )
        return {"status": "ok", "transaction": tx}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/rgs/credit")
def rgs_credit(req: SettleWinRequest):
    """Called by RGS to credit winnings to player wallet."""
    if req.payout <= 0:
        wallet = ledger.get_wallet(req.user_id)
        return {"status": "ok", "payout": 0.0, "balance_after": wallet["balance"]}
    
    tx = ledger.execute_ledger_transaction(
        user_id=req.user_id,
        tx_type="WIN",
        direction="CREDIT",
        amount=req.payout,
        reference_id=req.round_id,
        description=f"Payout for {req.game_id} round {req.round_id}"
    )
    return {"status": "ok", "transaction": tx}

@app.get("/api/v1/admin/stats")
def get_admin_stats(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    with ledger.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(balance) FROM wallets")
        total_wallets, total_bankroll = cursor.fetchone()
        
        cursor.execute("SELECT tx_type, SUM(amount), COUNT(*) FROM ledger_transactions lt JOIN ledger_entries le ON lt.id = le.transaction_id GROUP BY tx_type")
        tx_breakdown = cursor.fetchall()
        
    return {
        "total_players": total_wallets or 0,
        "total_vault_balance": round(total_bankroll or 0.0, 2),
        "transactions_summary": [
            {"type": row[0], "total_volume": round(row[1], 2), "count": row[2]} for row in tx_breakdown
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
