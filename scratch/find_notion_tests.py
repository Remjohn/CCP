import os

TESTS_DIR = r"d:\Work\The Conscious Coaching Factory\tests"
notion_tests = []

for root, dirs, files in os.walk(TESTS_DIR):
    for f in files:
        if not f.endswith('.py'):
            continue
        filepath = os.path.join(root, f)
        
        content = ""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                content = file_obj.read()
        except:
            pass
            
        if 'notion' in f.lower() or 'notion' in content.lower():
            rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
            notion_tests.append(rel_path)

print(f"Obsolete Notion Tests (Total found: {len(notion_tests)}):")
for t in notion_tests:
    print(f"  - {t}")
