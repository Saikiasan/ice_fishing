// ==UserScript==
// @name         Safe UI Balance Display Mock (Non-Intrusive)
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  Non-intrusive DOM visual replacement that does not hook WebSockets or trigger reload loops
// @match        *://*/*
// @run-at       document-end
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Desired mock string for UI layout testing
    const MOCK_DISPLAY_STRING = "₹ 20,000.00";

    /**
     * Non-intrusive text replacement:
     * We ONLY touch specific, already-rendered text elements that contain
     * the exact balance patterns, avoiding any interference with JavaScript loaders,
     * network sockets, or framework state objects.
     */
    function replaceRenderedBalance() {
        // 1. Target the Lobby Wallet container (Instamatch header button)
        const walletButton = document.querySelector('button[class*="wallet"], button:has(img[src*="Coin"])') ||
                             Array.from(document.querySelectorAll('button')).find(b => b.textContent && b.textContent.includes('MY WALLET'));

        if (walletButton) {
            // Find child nodes to preserve SVG icons/images
            const walker = document.createTreeWalker(walletButton, NodeFilter.SHOW_TEXT, null, false);
            let node;
            while ((node = walker.nextNode())) {
                const val = node.nodeValue;
                // Replace any pattern like "₹ 0.00" or similar amounts without destroying the button structure
                if (val && val.includes('₹')) {
                    node.nodeValue = val.replace(/₹\s*[\d,]+(\.\d{2})?/g, MOCK_DISPLAY_STRING);
                }
            }
        }

        // 2. Target the In-Game Balance Display (Evolution footer)
        // Evolution renders balance inside: span with class containing 'Balance' or 'text'
        const gameBalanceSpans = document.querySelectorAll('[data-role="balance-value"], [data-role="balance-label"], span[class*="Balance"]');
        gameBalanceSpans.forEach(span => {
            if (span.children.length === 0 && span.textContent && (span.textContent.includes('₹') || span.textContent.includes('0.'))) {
                span.textContent = MOCK_DISPLAY_STRING;
            }
        });
    }

    // Run periodically after page has loaded
    setInterval(replaceRenderedBalance, 800);

    console.log("[Safe Mock] Non-intrusive DOM visual replacement active.");
})();
