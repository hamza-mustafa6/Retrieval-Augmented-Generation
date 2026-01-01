from pathlib import Path 
import re
markdown_path = Path(__file__).parent/"Books/OnTheSufferings.md"
content = markdown_path.read_text(encoding='utf-8')
def clean_markdown_spaces(file_path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    content = file_path.read_text(encoding='utf-8')
    lines = [line.rstrip() for line in content.splitlines()]
    cleaned_content = "\n".join(lines)
    cleaned_content = re.sub(r' +', ' ', cleaned_content)
    file_path.write_text(cleaned_content, encoding='utf-8')
    print(f"Successfully cleaned: {file_path}")

clean_markdown_spaces(markdown_path)