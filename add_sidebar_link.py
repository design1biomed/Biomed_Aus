import re

template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\templates\biomed_app\dashboard\dashboard_base.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Email Config li and insert after it
pattern = r'(<li class="nav-item">\s*<a class="nav-link.*?href="\{% url \'dashboard_email_config\' %\}.*?>\s*<i class="bi bi-envelope-gear"></i>\s*Email Config\s*</a>\s*</li>)'

new_link = """\\1
              <li class="nav-item">
                  <a class="nav-link {% if 'event-subscribers' in request.path %}active{% endif %}"
                      href="{% url 'dashboard_event_subscribers' %}">
                      <i class="bi bi-person-lines-fill"></i> Event Subscribers
                  </a>
              </li>"""

if re.search(pattern, content):
    content = re.sub(pattern, new_link, content)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Sidebar updated successfully!")
else:
    print("Pattern not found. Checking exactly what it looks like:")
