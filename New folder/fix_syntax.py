template_path = r"c:\Users\Biomed\Documents\biomed\biomed_app\views.py"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_string = r"\1# Send beautifully designed notification email with resume attachment"
good_string = "application.save()\n              \n              # Send beautifully designed notification email with resume attachment"

if bad_string in content:
    content = content.replace(bad_string, good_string)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed the SyntaxError!")
else:
    print("Could not find the bad string.")
