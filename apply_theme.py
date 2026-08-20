import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\news_events.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the style block
old_style = r"<style>\s*\.notify-container \{.*?\}[\s\S]*?</style>"

new_style = """<style>
                .notify-container {
                    position: relative;
                    display: flex;
                    align-items: center;
                    height: 52px;
                }
                .notify-input-wrapper {
                    display: flex;
                    align-items: center;
                    background-color: #f8f9fa;
                    border: 1.5px solid #e9ecef;
                    border-radius: 50px;
                    padding: 4px 4px 4px 16px;
                    height: 100%;
                    min-width: 360px;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
                    opacity: 0;
                    transform: scale(0.9) translateX(20px);
                }
                .notify-input-wrapper.active {
                    opacity: 1;
                    transform: scale(1) translateX(0);
                }
                .notify-input-wrapper:focus-within {
                    border-color: #198754;
                    box-shadow: 0 0 0 4px rgba(25, 135, 84, 0.15);
                    background-color: #ffffff;
                }
                .notify-input-wrapper input {
                    border: none;
                    background: transparent;
                    padding: 0;
                    margin-right: 12px;
                    font-size: 16px;
                    outline: none;
                    flex: 1;
                    color: #212529;
                    width: 100%;
                }
                .notify-input-wrapper input::placeholder {
                    color: #adb5bd;
                    font-weight: 400;
                }
                #notifyInitBtn {
                    transition: all 0.2s ease-out;
                }
                </style>"""

content = re.sub(old_style, new_style, content)

# Replace the inner button
old_button_html = r'<button type="submit" class="notify-submit-btn">Notify Me</button>'
new_button_html = '<button type="submit" class="btn btn-success rounded-pill px-4 fw-semibold shadow-sm d-flex align-items-center" style="height: 100%;"><span class="d-none d-sm-inline me-1">Confirm</span><i class="fas fa-paper-plane ms-1"></i></button>'

content = content.replace(old_button_html, new_button_html)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Theme successfully applied!")
