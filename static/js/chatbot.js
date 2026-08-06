/* ═══════════════════════════════════════════════════════════
   chatbot.js — Bio Med Ingredients Floating Chat Widget
   ═══════════════════════════════════════════════════════════ */

(function () {
    'use strict';

    // ── Config ───────────────────────────────────────────────
    const API_URL = '/chatbot/api/';

    // ── State ────────────────────────────────────────────────
    let isOpen = false;
    let isWaiting = false;
    let mascotState = 'happy';
    let mascotParticleInterval = null;

    const mascotImages = {
        'happy': 2, 'greeting': 3, 'thinking': 4, 'listening': 5,
        'explaining': 6, 'excited': 7, 'surprised': 8, 'confused': 9,
        'sad': 10, 'laughing': 11, 'wink': 12, 'love': 13,
        'proud': 14, 'processing': 15, 'success': 16, 'error': 17,
        'sleep': 18, 'celebration': 19
    };

    // Preload images
    const preloadedImages = {};
    for (const state in mascotImages) {
        const img = new Image();
        img.src = `/media/chatbot/maArtboard%20${mascotImages[state]}.webp`;
        preloadedImages[state] = img;
    }

    // ── DOM refs (set in init) ───────────────────────────────
    let toggle, chatWindow, messages, input, sendBtn;

    // ── Helpers ──────────────────────────────────────────────
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    function formatAnswer(text) {
        // Convert **bold**, newlines → <br>, and basic lists
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    // ── Message rendering ────────────────────────────────────
    function addMessage(text, role) {
        const msg = document.createElement('div');
        msg.className = `bm-msg ${role}`;

        if (role === 'bot') {
            msg.innerHTML = `
                <div class="bm-msg-avatar"><i class="bi bi-cpu"></i></div>
                <div class="bm-bubble">${formatAnswer(text)}</div>
            `;
        } else {
            msg.innerHTML = `
                <div class="bm-msg-avatar" style="background:linear-gradient(135deg,#4a90d9,#2c5f8a);">
                    <i class="bi bi-person-fill"></i>
                </div>
                <div class="bm-bubble">${escapeHtml(text)}</div>
            `;
        }

        messages.appendChild(msg);
        scrollToBottom();
        return msg;
    }

    function showTyping() {
        const typing = document.createElement('div');
        typing.className = 'bm-msg bot bm-typing';
        typing.id = 'bm-typing-indicator';
        typing.innerHTML = `
            <div class="bm-msg-avatar"><i class="bi bi-cpu"></i></div>
            <div class="bm-bubble">
                <div class="bm-dot"></div>
                <div class="bm-dot"></div>
                <div class="bm-dot"></div>
            </div>
        `;
        messages.appendChild(typing);
        scrollToBottom();
    }

    function removeTyping() {
        const t = document.getElementById('bm-typing-indicator');
        if (t) t.remove();
    }

    // ── Mascot State Management ──────────────────────────────
    function setMascotState(newState) {
        const wrapper = document.getElementById('bm-mascot-container');
        const img = document.getElementById('bm-mascot-img');
        const particlesContainer = document.getElementById('bm-particles-container');
        if (!wrapper || !img) return;

        wrapper.classList.remove(`bm-state-${mascotState}`);
        mascotState = newState;
        wrapper.classList.add(`bm-state-${mascotState}`);

        if (mascotImages[newState]) {
            img.classList.remove('bm-pop-anim');
            void img.offsetWidth; // trigger reflow
            img.classList.add('bm-pop-anim');
            img.src = `/media/chatbot/maArtboard%20${mascotImages[newState]}.webp`;
        }

        handleMascotParticles(mascotState, particlesContainer);
    }

    function handleMascotParticles(state, container) {
        if (mascotParticleInterval) {
            clearInterval(mascotParticleInterval);
            mascotParticleInterval = null;
        }
        container.innerHTML = '';
        if (state === 'excited' || state === 'success') spawnMascotParticles(container, 'bm-particle-sparkle', 300);
        else if (state === 'love') spawnMascotParticles(container, 'bm-particle-heart', 400);
        else if (state === 'thinking' || state === 'confused') spawnMascotParticles(container, 'bm-particle-question', 600);
        else if (state === 'sleep') spawnMascotParticles(container, 'bm-particle-zzz', 800);
        else if (state === 'celebration') {
            for (let i = 0; i < 20; i++) createSingleParticle(container, 'bm-particle-confetti');
            spawnMascotParticles(container, 'bm-particle-confetti', 100);
        }
    }

    function spawnMascotParticles(container, className, interval) {
        mascotParticleInterval = setInterval(() => {
            createSingleParticle(container, className);
        }, interval);
    }

    function createSingleParticle(container, className) {
        const p = document.createElement('div');
        p.className = `bm-particle ${className}`;
        const xOffset = (Math.random() - 0.5) * 120;
        const yOffset = (Math.random() - 0.5) * 120 - 20;
        p.style.left = `calc(50% + ${xOffset}px)`;
        p.style.top = `calc(50% + ${yOffset}px)`;
        container.appendChild(p);
        setTimeout(() => p.remove(), 2000);
    }

    // ── Send message ─────────────────────────────────────────
    async function sendMessage(text) {
        if (isWaiting || !text.trim()) return;

        const userText = text.trim();
        input.value = '';
        input.style.height = 'auto';

        addMessage(userText, 'user');
        showTyping();
        isWaiting = true;
        sendBtn.disabled = true;
        setMascotState('processing');

        try {
            const resp = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ 
                    message: userText, 
                    current_page: window.location.pathname,
                    page_text: document.body.innerText.substring(0, 3000)
                })
            });

            removeTyping();

            if (resp.ok) {
                const data = await resp.json();
                const botMsg = data.answer || data.error || 'Sorry, no response available.';
                addMessage(botMsg, 'bot');

                // Determine appropriate animation state based on AI's parsed emotion
                let replyState = data.emotion || 'explaining';
                
                // Fallback for network/backend errors
                if (data.error) {
                    replyState = 'error';
                }

                setMascotState(replyState);
                
                // Hold the emotional state until the next interaction
            } else {
                addMessage('An error occurred. Please try again.', 'bot');
                setMascotState('error');
                setTimeout(() => { if (mascotState === 'error') setMascotState('happy'); }, 3000);
            }
        } catch (error) {
            removeTyping();
            addMessage('A network error occurred.', 'bot');
            setMascotState('error');
            setTimeout(() => { if (mascotState === 'error') setMascotState('happy'); }, 3000);
            console.error('[BioMed Chatbot] Error:', error);
        } finally {
            isWaiting = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }

    // ── CSRF token ───────────────────────────────────────────
    function getCsrfToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1].trim() : '';
    }

    // ── Open / Close ─────────────────────────────────────────
    function openChat() {
        isOpen = true;
        chatWindow.classList.add('open');
        toggle.classList.add('active');
        toggle.setAttribute('aria-label', 'Close chat');
        setTimeout(() => input.focus(), 350);

        // Greet when opened
        setMascotState('greeting');
        setTimeout(() => { if (mascotState === 'greeting') setMascotState('happy'); }, 2500);
    }

    function closeChat() {
        isOpen = false;
        chatWindow.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-label', 'Open chat');

        // Go to sleep when closed
        setMascotState('sleep');
    }

    function toggleChat() {
        isOpen ? closeChat() : openChat();
    }

    // ── Quick suggestion chips ───────────────────────────────
    function bindSuggestions() {
        document.querySelectorAll('.bm-suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                sendMessage(chip.textContent.trim());
            });
        });
    }



    // ── Build HTML ───────────────────────────────────────────
    function buildWidget() {
        // Toggle button
        const btn = document.createElement('img');
        btn.id = 'bm-chat-toggle';
        btn.src = window.CHATBOT_ICON_URL || '/static/images/BMI Logo.webp';
        btn.alt = 'Chat';
        btn.setAttribute('role', 'button');
        btn.setAttribute('aria-label', 'Open chat');
        btn.style.background = 'none';
        btn.style.boxShadow = 'none';
        btn.style.borderRadius = '0';
        btn.style.width = '65px';
        btn.style.height = '65px';
        btn.style.objectFit = 'contain';

        // Chat window
        const win = document.createElement('div');
        win.id = 'bm-chat-window';
        win.setAttribute('role', 'dialog');
        win.setAttribute('aria-label', 'Bio Med Chat Assistant');
        win.innerHTML = `
            <div id="bm-chat-header">
                <div class="bm-avatar" style="background: transparent; display: flex; align-items: center; justify-content: center; padding: 4px;">
                    <div id="bm-mascot-container" class="bm-state-happy">
                        <div class="bm-particles-container" id="bm-particles-container"></div>
                        <div class="bm-character">
                            <img id="bm-mascot-img" src="/media/chatbot/maArtboard%202.webp" alt="Mascot">
                        </div>
                    </div>
                </div>
                <div class="bm-header-info">
                    <h6>Bio Med Assistant</h6>
                    <span>
                        <span class="bm-online-dot"></span> Online — Ask me anything
                    </span>
                </div>
                <div class="bm-header-actions">
                    <button class="bm-header-btn" id="bm-clear-btn" title="Clear chat">
                        <i class="bi bi-arrow-counterclockwise"></i>
                    </button>
                    <button class="bm-header-btn" id="bm-close-btn" title="Close chat">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>

            <div id="bm-messages">
                <div class="bm-welcome-card">
                    <strong>👋 Hello! I'm the Bio Med Assistant.</strong>
                    I can answer questions about our products, ingredients, certifications, and more. How can I help you today?
                    <div class="bm-suggestions">
                        <span class="bm-suggestion-chip">What is Curcumin?</span>
                        <span class="bm-suggestion-chip">Herbal extracts range</span>
                        <span class="bm-suggestion-chip">Certifications</span>
                        <span class="bm-suggestion-chip">Job openings</span>
                    </div>
                </div>
            </div>

            <div id="bm-chat-footer">
                <textarea
                    id="bm-input"
                    placeholder="Type your question..."
                    rows="1"
                    aria-label="Chat message"
                    maxlength="1000"
                ></textarea>
                <button id="bm-send-btn" aria-label="Send message">
                    <i class="bi bi-send-fill"></i>
                </button>
            </div>
        `;

        document.body.appendChild(btn);
        document.body.appendChild(win);
    }

    // ── Init ─────────────────────────────────────────────────
    function init() {
        buildWidget();

        toggle = document.getElementById('bm-chat-toggle');
        chatWindow = document.getElementById('bm-chat-window');
        messages = document.getElementById('bm-messages');
        input = document.getElementById('bm-input');
        sendBtn = document.getElementById('bm-send-btn');

        // Toggle
        toggle.addEventListener('click', toggleChat);

        // Close button (header)
        document.getElementById('bm-close-btn').addEventListener('click', closeChat);

        // Clear button
        document.getElementById('bm-clear-btn').addEventListener('click', () => {
            messages.innerHTML = `
                <div class="bm-welcome-card">
                    <strong>👋 Hello! I'm the Bio Med Assistant.</strong>
                    I can answer questions about our products, ingredients, certifications, and more. How can I help you today?
                    <div class="bm-suggestions">
                        <span class="bm-suggestion-chip">What is Curcumin?</span>
                        <span class="bm-suggestion-chip">Herbal extracts range</span>
                        <span class="bm-suggestion-chip">Certifications</span>
                        <span class="bm-suggestion-chip">Job openings</span>
                    </div>
                </div>
            `;
            bindSuggestions();
        });

        // Send on button click
        sendBtn.addEventListener('click', () => sendMessage(input.value));

        // Send on Enter (Shift+Enter = newline)
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage(input.value);
            }
        });

        // Auto-resize textarea and change state to listening
        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 100) + 'px';

            if (input.value.trim().length > 0) {
                if (mascotState !== 'listening') setMascotState('listening');
            } else {
                if (mascotState !== 'happy') setMascotState('happy');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) closeChat();
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (isOpen && !chatWindow.contains(e.target) && !toggle.contains(e.target)) {
                closeChat();
            }
        });

        // Bind suggestion chips
        bindSuggestions();

        // ── Interactive Mouse Tracking (Parallax) ──
        let cachedCenterX = 0, cachedCenterY = 0;
        let isRectCached = false;
        
        window.addEventListener('resize', () => isRectCached = false);

        document.addEventListener('mousemove', (e) => {
            if (!isOpen) {
                isRectCached = false;
                return;
            }
            const wrapper = document.getElementById('bm-mascot-container');
            if (wrapper) {
                if (!isRectCached) {
                    const rect = wrapper.getBoundingClientRect();
                    cachedCenterX = rect.left + rect.width / 2;
                    cachedCenterY = rect.top + rect.height / 2;
                    isRectCached = true;
                }
                const xAxis = (cachedCenterX - e.clientX) / 20;
                const yAxis = (cachedCenterY - e.clientY) / 20;
                wrapper.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
            }
        });

        document.addEventListener('mouseleave', () => {
            const wrapper = document.getElementById('bm-mascot-container');
            if (wrapper) wrapper.style.transform = `rotateY(0deg) rotateX(0deg)`;
        });

        // ── Mascot Interaction (Click) ──
        setTimeout(() => {
            const mascotImg = document.getElementById('bm-mascot-img');
            if (mascotImg) {
                mascotImg.addEventListener('click', () => {
                    const reactions = ['surprised', 'excited', 'laughing', 'confused'];
                    const randomReaction = reactions[Math.floor(Math.random() * reactions.length)];
                    setMascotState(randomReaction);
                    setTimeout(() => { if (mascotState === randomReaction) setMascotState('happy'); }, 2000);
                });
            }
        }, 100);
    }

    // Run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
