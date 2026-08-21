import os

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\news_events.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """            <div class="col-md-12 col-lg-6 col-xl-5 mb-3 mb-md-4 mb-lg-0 text-center text-lg-start">
                <h3 class="fw-bold text-dark mb-2" style="font-size: 24px;">Welcome to</h3>
                <h3 class="fw-bold text-success" style="font-size: 24px;">Our News and Event Site</h3>
            </div>"""

new_text = """            <div class="col-md-12 col-lg-6 col-xl-5 mb-3 mb-md-4 mb-lg-0 text-center text-lg-start">
                <h3 class="fw-bold text-dark mb-2" style="font-size: 24px;">Welcome to</h3>
                <h3 class="fw-bold text-success" style="font-size: 24px;">Our News and Event Site</h3>
                <p class="text-muted mt-3 mb-0" style="font-size: 0.95rem; line-height: 1.5;">
                    <i class="fas fa-envelope-open-text text-success me-2"></i>Stay in the loop! Subscribe with your email to receive instant notifications whenever we announce new exhibitions or events.
                </p>
            </div>"""

if target in content:
    content = content.replace(target, new_text)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Subscription text added successfully!")
else:
    print("Target text not found.")
