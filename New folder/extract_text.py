import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
        self.hide = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'head', 'title', 'meta'):
            self.hide = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'head', 'title', 'meta'):
            self.hide = False

    def handle_data(self, d):
        if not self.hide:
            self.text.append(d)

    def get_data(self):
        return ''.join(self.text)

try:
    with open('C:\\Users\\Biomed\\.gemini\\antigravity-ide\\brain\\e79a94a9-dadf-4855-8608-9c3c59734912\\scratch\\previous_index_raw.html', 'r', encoding='utf-8') as f:
        html = f.read()
    s = MLStripper()
    s.feed(html)
    lines = [t.strip() for t in s.get_data().split('\n') if t.strip()]
    unique_lines = []
    for line in lines:
        if line and line not in unique_lines and len(line) > 3 and '{' not in line:
            unique_lines.append(line)
    
    with open('extracted_content.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(unique_lines[:150]))
    print('Extraction complete.')
except Exception as e:
    print(f'Error: {e}')
