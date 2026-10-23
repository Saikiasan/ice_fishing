with open('evo_server/frontend/evo/r3/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's check if our helper script is already present
if 'window.__WS_BALANCE_SYNC__' in c:
    print("Already present in index.html")
else:
    sync_script = '''<script>
// Real-time WebSocket Balance Synchronization Engine
(function() {
    window.__WS_BALANCE_SYNC__ = true;
    window.__LIVE_BALANCE__ = null;
    window.__TOTAL_BET__ = 0;

    function formatINR(val) {
        try {
            return "₹" + Number(val).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } catch(e) {
            return "₹" + Number(val).toFixed(2);
        }
    }

    function syncDOMBalance(newBalance) {
        if (typeof newBalance !== "number" || isNaN(newBalance)) return;
        window.__LIVE_BALANCE__ = newBalance;
        window.dispatchEvent(new CustomEvent("live_balance_changed", { detail: { balance: newBalance } }));

        var formatted = formatINR(newBalance);
        
        // 1. Target all data-role="balance-value" elements
        var valEls = document.querySelectorAll('[data-role="balance-value"]');
        valEls.forEach(function(el) {
            el.textContent = formatted;
            el.setAttribute("data-balance-visible", formatted);
        });

        // 2. Also check any balance label containers
        var labels = document.querySelectorAll('[data-role="balance-label-one-line"], [data-role="balance-label"]');
        labels.forEach(function(el) {
            var v = el.querySelector('[data-role="balance-value"]') || el.querySelector('.value, span:last-child');
            if (v && v.getAttribute('data-role') === 'balance-value') {
                v.textContent = formatted;
            }
        });
    }

    window.__syncDOMBalance = syncDOMBalance;

    // Intercept Native WebSocket to monitor balanceUpdated and icefishing.bets in real time
    var OrigWebSocket = window.WebSocket;
    window.WebSocket = function(url, protocols) {
        var ws = protocols !== undefined ? new OrigWebSocket(url, protocols) : new OrigWebSocket(url);
        
        ws.addEventListener('message', function(event) {
            try {
                if (typeof event.data !== "string") return;
                var msg = JSON.parse(event.data);
                var type = msg.type || (msg.payload && msg.payload.type);

                // Check for balanceUpdated frame
                if (type === "balanceUpdated") {
                    var bal = (msg.payload && typeof msg.payload.balance === "number") ? msg.payload.balance :
                              (msg.args && typeof msg.args.balance === "number") ? msg.args.balance : null;
                    if (bal !== null) {
                        syncDOMBalance(bal);
                    }
                }
                // Check for icefishing.bets frame (Accepted, Settled, NoBets)
                else if (type === "icefishing.bets") {
                    var state = (msg.payload && msg.payload.state) || (msg.args && msg.args.state);
                    if (state && typeof state.balance === "number") {
                        syncDOMBalance(state.balance);
                    }
                }
            } catch(e) {}
        });

        return ws;
    };
    window.WebSocket.prototype = OrigWebSocket.prototype;
    window.WebSocket.CONNECTING = OrigWebSocket.CONNECTING;
    window.WebSocket.OPEN = OrigWebSocket.OPEN;
    window.WebSocket.CLOSING = OrigWebSocket.CLOSING;
    window.WebSocket.CLOSED = OrigWebSocket.CLOSED;

    // Periodic safeguard loop ensuring DOM never reverts or lags
    setInterval(function() {
        if (typeof window.__LIVE_BALANCE__ === "number") {
            var formatted = formatINR(window.__LIVE_BALANCE__);
            var valEls = document.querySelectorAll('[data-role="balance-value"]');
            valEls.forEach(function(el) {
                if (el.textContent !== formatted) {
                    el.textContent = formatted;
                    el.setAttribute("data-balance-visible", formatted);
                }
            });
        }
    }, 250);
})();
</script>'''

    pos = c.find('</head>')
    c = c[:pos] + sync_script + c[pos:]
    with open('evo_server/frontend/evo/r3/index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully injected WebSocket real-time balance sync engine into index.html!")
