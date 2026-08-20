import os
import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\news_events.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_button = """                <button type="button" data-bs-toggle="modal" data-bs-target="#notifyModal"
                    class="btn btn-success btn-lg rounded-pill px-3 px-md-4 py-2 fw-semibold d-flex align-items-center shadow-sm">
                    Notify me
                    <i class="fas fa-bell ms-2"></i>
                </button>"""

new_ui = """                <!-- Interactive Notify Component -->
                <style>
                .notify-container {
                    position: relative;
                    display: flex;
                    align-items: center;
                    height: 52px;
                }
                .notify-input-wrapper {
                    display: flex;
                    align-items: center;
                    background-color: #f4f4f5;
                    border-radius: 50px;
                    padding: 6px;
                    height: 100%;
                    min-width: 320px;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1); /* Slight bounce */
                    opacity: 0;
                    transform: scale(0.9) translateX(20px);
                }
                .notify-input-wrapper.active {
                    opacity: 1;
                    transform: scale(1) translateX(0);
                }
                .notify-input-wrapper input {
                    border: none;
                    background: transparent;
                    padding: 0 16px;
                    font-size: 16px;
                    outline: none;
                    flex: 1;
                    color: #333;
                    width: 100%;
                }
                .notify-input-wrapper input::placeholder {
                    color: #a0a0a0;
                }
                .notify-submit-btn {
                    background-color: #ffffff;
                    color: #000000;
                    border: none;
                    border-radius: 50px;
                    padding: 8px 24px;
                    font-weight: 600;
                    font-size: 15px;
                    cursor: pointer;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                    transition: all 0.2s;
                    white-space: nowrap;
                    height: 100%;
                }
                .notify-submit-btn:hover {
                    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
                    transform: translateY(-1px);
                }
                #notifyInitBtn {
                    transition: all 0.2s ease-out;
                }
                </style>

                <div class="notify-container" id="notifyContainer">
                    <!-- Initial Button -->
                    <button type="button" id="notifyInitBtn"
                        class="btn btn-success btn-lg rounded-pill px-3 px-md-4 py-2 fw-semibold d-flex align-items-center shadow-sm">
                        Notify me
                        <i class="fas fa-bell ms-2"></i>
                    </button>

                    <!-- Expandable Form (Hidden initially) -->
                    <form action="{% url 'subscribe_event_notifications' %}" method="POST" id="notifyInlineForm" class="d-none m-0">
                        {% csrf_token %}
                        <div class="notify-input-wrapper shadow-sm">
                            <input type="email" name="email" id="notifyInlineEmail" placeholder="Email" required autocomplete="email">
                            <button type="submit" class="notify-submit-btn">Notify Me</button>
                        </div>
                    </form>
                </div>

                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const notifyBtn = document.getElementById('notifyInitBtn');
                    const notifyForm = document.getElementById('notifyInlineForm');
                    const notifyWrapper = document.querySelector('.notify-input-wrapper');
                    const notifyEmail = document.getElementById('notifyInlineEmail');

                    if(notifyBtn && notifyForm) {
                        notifyBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            // Hide initial button
                            notifyBtn.classList.add('d-none');
                            // Show form
                            notifyForm.classList.remove('d-none');
                            
                            // Trigger animation in next frame
                            setTimeout(() => {
                                notifyWrapper.classList.add('active');
                                notifyEmail.focus();
                            }, 10);
                        });
                        
                        // Click outside to close (revert to button)
                        document.addEventListener('click', function(e) {
                            if (!notifyForm.classList.contains('d-none') && 
                                !document.getElementById('notifyContainer').contains(e.target)) {
                                
                                notifyWrapper.classList.remove('active');
                                setTimeout(() => {
                                    notifyForm.classList.add('d-none');
                                    notifyBtn.classList.remove('d-none');
                                }, 300); // Wait for transition
                            }
                        });
                    }
                });
                </script>"""

if target_button in content:
    content = content.replace(target_button, new_ui)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("UI successfully applied!")
else:
    print("Could not find the target button in the HTML.")
