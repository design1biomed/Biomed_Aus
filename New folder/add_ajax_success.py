import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\news_events.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new JS to replace the old script block inside the component section
# We will match the entire script block that starts with <script> and ends with </script>
# specifically the one handling notifyInitBtn

old_script_pattern = re.compile(r"<script>\s*document\.addEventListener\('DOMContentLoaded', function \(\) \{\s*const notifyBtn = document\.getElementById\('notifyInitBtn'\);.*?\}\);\s*</script>", re.DOTALL)

new_script = """<script>
                document.addEventListener('DOMContentLoaded', function () {
                    const notifyBtn = document.getElementById('notifyInitBtn');
                    const notifyForm = document.getElementById('notifyInlineForm');
                    const notifyWrapper = document.querySelector('.notify-input-wrapper');
                    const notifyEmail = document.getElementById('notifyInlineEmail');

                    if (notifyBtn && notifyForm) {
                        notifyBtn.addEventListener('click', function (e) {
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
                        document.addEventListener('click', function (e) {
                            if (!notifyForm.classList.contains('d-none') &&
                                !document.getElementById('notifyContainer').contains(e.target)) {

                                notifyWrapper.classList.remove('active');
                                setTimeout(() => {
                                    notifyForm.classList.add('d-none');
                                    notifyBtn.classList.remove('d-none');
                                }, 300); // Wait for transition
                            }
                        });

                        // Handle AJAX form submission for a sleek inline success message
                        notifyForm.addEventListener('submit', function (e) {
                            e.preventDefault();
                            const formData = new FormData(notifyForm);
                            const submitBtn = notifyForm.querySelector('button[type="submit"]');
                            const originalBtnHtml = submitBtn.innerHTML;
                            
                            // Set button to loading state
                            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
                            submitBtn.disabled = true;

                            fetch(notifyForm.action, {
                                method: 'POST',
                                body: formData,
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                }
                            }).then(response => {
                                // Transform the wrapper into a success message!
                                notifyWrapper.innerHTML = '<div class="w-100 text-center text-success fw-bold" style="font-size: 1.1rem; padding: 4px 0;"><i class="fas fa-check-circle me-2"></i> Subscribed successfully!</div>';
                                
                                // Close and reset after 3 seconds
                                setTimeout(() => {
                                    notifyWrapper.classList.remove('active');
                                    setTimeout(() => {
                                        // Reload page to show Django messages or reset UI completely
                                        window.location.reload();
                                    }, 300);
                                }, 3000);
                            }).catch(error => {
                                submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
                                submitBtn.classList.replace('btn-success', 'btn-danger');
                                setTimeout(() => {
                                    submitBtn.innerHTML = originalBtnHtml;
                                    submitBtn.disabled = false;
                                    submitBtn.classList.replace('btn-danger', 'btn-success');
                                }, 3000);
                            });
                        });
                    }
                });
                </script>"""

if old_script_pattern.search(content):
    content = old_script_pattern.sub(new_script.replace('\\', '\\\\'), content, count=1)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("AJAX script successfully applied!")
else:
    print("Could not find the script block to replace.")
