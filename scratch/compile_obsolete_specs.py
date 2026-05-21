import os

DOCS_DIR = r"d:\Work\The Conscious Coaching Factory\docs\architecture"

obsolete_specs = []

for root, dirs, files in os.walk(DOCS_DIR):
    # Skip the april_updates directory since those are the active Era 3 specs (the updates)
    if 'april_updates' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
        
        # Check content of the spec file
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                content = file_obj.read()
            
            first_few_lines = "\n".join(content.split("\n")[:10]).lower()
            
            # Look for explicit flags
            is_obsolete = False
            reason = ""
            
            if 'superseded' in first_few_lines or 'superseded' in content.lower()[:300]:
                is_obsolete = True
                reason = "Header indicates it is superseded"
            elif 'deprecated' in first_few_lines or 'deprecated' in content.lower()[:300]:
                is_obsolete = True
                reason = "Header indicates it is deprecated"
            elif 'obsolete' in first_few_lines or 'obsolete' in content.lower()[:300]:
                is_obsolete = True
                reason = "Header indicates it is obsolete"
            elif any(kw in f.lower() for kw in ['trivianar', 'canva', 'webrtc', 'notion_export', 'notion_card']):
                is_obsolete = True
                reason = "Filename matches deprecated system (Trivianar/Canva/WebRTC/Notion)"
            
            if is_obsolete:
                obsolete_specs.append((rel_path, reason))
        except:
            pass

print(f"Obsolete/Deprecated Technical Specs (Found {len(obsolete_specs)} specs):")
for path, reason in sorted(obsolete_specs):
    print(f"  - {path}: {reason}")
