# Executive Dashboard & Real-Time Financial KPIs

## 1. Executive Persona & Purpose

The Financial Executive Dashboard provides the Chief Financial Officer (CFO), VP of Finance, Head of Payments, and Treasury Managers an instantaneous cockpit to evaluate platform solvency, profitability, game math behavior, and liquidity flows in real time.

---

## 2. Key Metrics & Formula Catalog

| Metric | Business Definition | Calculation Formula | Refresh Frequency | Target SLA / Tolerance |
|---|---|---|---|---|
| **Turnover (Total Bets)** | Gross handle wagered across all active games. | `∑ Bets.amount` | Real-time (<500ms) | Track growth vs forecast |
| **Gross Gaming Revenue (GGR)** | Platform win before bonuses and taxes. | `Turnover - Total Wins` | Real-time (<500ms) | Alert on negative hourly drift |
| **Net Gaming Revenue (NGR)** | True net earnings after bonuses, PSP fees, and royalities. | `GGR - Bonus Costs - PSP Fees - Royalties - Gaming Tax` | Hourly / EOD | Stable margin (15% - 28%) |
| **Actual RTP vs. Theoretical RTP** | Realized payout percentage vs configured game RTP (e.g. 96.0%). | `(Total Wins / Total Bets) * 100` | Rolling 15m, 1h, 24h, 30d | Alert if deviation > 3.5% over 10k spins |
| **Player Balance Liability** | Aggregate cash balance residing in player wallets (unspent funds). | `∑ PlayerWallet.cash_balance` | Real-time (<2s) | Solvency coverage ratio ≥ 120% |
| **PSP Approval Rate** | Percentage of initiated deposits successfully settled. | `(Successful Deposits / Attempted Deposits) * 100` | Rolling 5m | Alert if < 85% |
| **Net Cash Flow** | Net liquidity gained/lost via banking channels. | `Deposits Settled - Withdrawals Settled - PSP Fees` | Real-time (<10s) | Continuous positive delta |
| **Withdrawal Processing SLA** | Median time taken from player cashout request to payout execution. | `Median(Settlement_Time - Request_Time)` | Real-time | Auto: < 2 min; Manual: < 30 min |

---

## 3. UI/UX Layout Specifications

The web client is designed as a single-page responsive application with high-contrast executive dark mode and live WebSocket push feeds.

```
+-----------------------------------------------------------------------------------------------------+
| [LOGO] FIN-EXEC CONSOLE          [Currency: USD | UTC]    [LIVE: 2,491 Players]    [ALERT: 1 Active] |
+-----------------------------------------------------------------------------------------------------+
| [TOP TICKER CARDS]                                                                                  |
|  TODAY'S TURNOVER     GGR (HOLD %)       LIVE RTP (DEV)       UNSETTLED WITHDRAWALS   NET CASH FLOW |
|  $1,248,320.00        $112,490 (9.01%)   90.99% (-0.51%)      $34,120.00 (14 tx)      +$280,410.00  |
+-----------------------------------------------------------------------------------------------------+
| [LIVE REVENUE & RTP TELEMETRY CHART]                 | [PSP LIQUIDITY & HEALTH]                     |
|                                                      |  Stripe:      $120,400 [98.2% OK]            |
|  (Time Series: Bets, Wins, GGR over rolling 24h)     |  Adyen:       $85,200  [97.1% OK]            |
|  --------------------------------------------------  |  Crypto Pool: $340,900 [Auto-rebalance ON]   |
|  [RTP Confidence Band: 96.0% ± 2.5%]                 |  Pix/Boleto:  $45,000  [91.4% WARNING]       |
+-----------------------------------------------------------------------------------------------------+
| [GAME ROOM BREAKDOWN TABLE]                          | [ACTIONABLE FRAUD & PAYOUT QUEUE]            |
|  Game           Turnover    GGR      RTP    Status   |  TxID     User    Amount    Risk   Action    |
|  Ice Fishing    $890,200    $80,120  91.0%  Normal   |  #9021    U881    $1,200    Low    [Approve] |
|  Ice Fishing EX $358,120    $32,370  90.9%  Normal   |  #9022    U419    $8,500    HIGH   [Review]  |
+-----------------------------------------------------------------------------------------------------+
```

---

## 4. Alerting & Threshold Hierarchy

1. **P0 - Critical Financial Threat (Instant SMS, PagerDuty, Telegram & UI Banner)**
   - Game RTP > 108% over a sliding 1,000-spin window (possible exploit or corrupted configuration).
   - Hot wallet liquidity drops below 15% of daily withdrawal demand.
   - Aggregate player balance jump > $50,000 within 5 minutes without corresponding verified deposits.
2. **P1 - Operational Degraded State (Slack & UI Toast)**
   - PSP settlement failure rate exceeds 15% on any single channel.
   - Payout queue SLA exceeds 45 minutes for verified players.
3. **P2 - Business Performance Warnings (Email Digest)**
   - Daily GGR down > 20% compared to 7-day trailing average.
   - Elevated chargeback notifications from credit card processors (> 0.65%).
