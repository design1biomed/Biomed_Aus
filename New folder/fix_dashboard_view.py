import os

filepath = r"c:\Users\Biomed\Documents\biomed\biomed_app\dashboard_views.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the wrong order_by field
old_line = "subscribers = EventSubscriber.objects.all().order_by('-created_at')"
new_line = "subscribers = EventSubscriber.objects.all().order_by('-subscribed_at')"

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed order_by in dashboard_views.py!")
else:
    print("Could not find the exact line. Let's check with regex.")
    
    import re
    if re.search(r"order_by\('-created_at'\)", content):
        content = re.sub(r"order_by\('-created_at'\)", "order_by('-subscribed_at')", content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed order_by using regex in dashboard_views.py!")
