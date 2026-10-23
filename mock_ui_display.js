// ==UserScript==
// @name         Local UI Balance Display Mock (Frontend QA Only)
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Educational demonstration of client-side DOM mocking and WebSocket event interception
// @match        *://*/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // The desired mock value to display locally for UI testing
    const MOCK_BALANCE = "₹ 20,000.00";

    /**
     * 1. DOM Mutation Observer:
     * Periodically or reactively replaces rendered balance text in the DOM.
     * This demonstrates why client-side DOM manipulation only changes visual pixels,
     * without affecting backend database records.
     */
    function updateDOMDisplay() {
        // Target common wallet button/label elements
        const walletButtons = document.querySelectorAll('button, div, span');
        walletButtons.forEach(el => {
            // Check if element contains wallet or balance indicators
            if (el.textContent && el.textContent.includes('MY WALLET') && el.textContent.includes('₹')) {
                // Example pattern: "MY WALLET ₹ 0.00 EXPOSURE ₹ 0.00 AVAILABLE ₹ 0.00"
                el.innerText = `MY WALLET ${MOCK_BALANCE} EXPOSURE ₹ 0.00 AVAILABLE ${MOCK_BALANCE}`;
            }
            // In-game iframe footer balance labels
            if (el.className && typeof el.className === 'string' && el.className.toLowerCase().includes('balance')) {
                const text = el.innerText || '';
                if (text.includes('₹') || text.toLowerCase().includes('balance')) {
                    el.innerText = `Balance: ${MOCK_BALANCE}`;
                }
            }
        });
    }

    // Set up an interval or MutationObserver to maintain visual display during local testing
    setInterval(updateDOMDisplay, 1000);

    /**
     * 2. WebSocket Packet Interception:
     * Demonstrates how the browser handles incoming JSON frames.
     * When the server sends a 'balanceUpdated' event, this hook intercepts
     * the incoming data stream in browser memory before it reaches the UI view layer.
     */
    const OriginalWebSocket = window.WebSocket;
    window.WebSocket = new Proxy(OriginalWebSocket, {
        construct(target, args) {
            const ws = new target(...args);

            ws.addEventListener('message', (event) => {
                try {
                    // Check if the incoming payload is a JSON balance update
                    if (typeof event.data === 'string' && event.data.includes('"balanceUpdated"')) {
                        console.log("[QA Demo] Intercepted incoming server balance event:", event.data);
                        // Notice: Altering this packet locally does NOT change the server's database.
                        // When a wager is submitted, the server evaluates its own internal state,
                        // completely bypassing client-side variables.
                    }
                } catch (e) {}
            });

            return ws;
        }
    });

    console.log("[QA Demo] Frontend display mock loaded. Visual rendering altered locally only.");
})();
