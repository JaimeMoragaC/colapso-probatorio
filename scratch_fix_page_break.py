import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip() == "---" and lines[i+2].strip() == '<div style="page-break-before: always;"></div>':
        skip = True
        continue
    if skip and line.strip() == '<div style="page-break-before: always;"></div>':
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

# Remove extra newlines
new_content = "".join(new_lines)
while "\n\n\n" in new_content:
    new_content = new_content.replace("\n\n\n", "\n\n")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
