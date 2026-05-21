import os
import re

SRC_DIR = r"d:\Work\The Conscious Coaching Factory\src"

notion_references = []

for root, dirs, files in os.walk(SRC_DIR):
    for f in files:
        if not f.endswith('.py'):
            continue
        filepath = os.path.join(root, f)
        
        # Check if notion is in filename
        in_filename = 'notion' in f.lower()
        
        # Check if notion is in file content
        content = ""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                content = file_obj.read()
        except:
            pass
            
        in_content = 'notion' in content.lower()
        
        if in_filename or in_content:
            rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
            # Count occurrences of "notion" (case-insensitive)
            count = len(re.findall(r'notion', content, re.IGNORECASE))
            notion_references.append({
                "file": rel_path,
                "in_filename": in_filename,
                "occurrences": count
            })

print(f"Audit of Notion-related code (Total found: {len(notion_references)}):")
for item in sorted(notion_references, key=lambda x: x["occurrences"], reverse=True):
    print(f"  - {item['file']}: {item['occurrences']} occurrences (In Filename: {item['in_filename']})")
