import os

TARGET_DIRS = [
    r"d:\Work\The Conscious Coaching Factory\src\ccp",
    r"d:\Work\The Conscious Coaching Factory\tests"
]
EXCLUDED_DIRS = {'.git', '.venv', 'node_modules', 'primitives', '.pytest_cache', '__pycache__', 'dist', '.system_generated'}
OBSOLETE_KEYWORDS = ['notion', 'trivianar', 'webrtc', 'canva']

code_obsolete_files = []

for base_dir in TARGET_DIRS:
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in files:
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
            
            # Check if filename matches keyword
            matched = False
            for kw in OBSOLETE_KEYWORDS:
                if kw in f.lower():
                    code_obsolete_files.append((rel_path, f"Filename contains '{kw}'"))
                    matched = True
                    break
                    
            if not matched and f.endswith(('.py', '.json')):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        content = file_obj.read()
                    for kw in OBSOLETE_KEYWORDS:
                        if kw in content.lower():
                            if any(term in content.lower() for term in ['import ', 'class ', 'def ']) or 'config' in f.lower() or 'test_' in f:
                                code_obsolete_files.append((rel_path, f"Content references '{kw}'"))
                                break
                except:
                    pass

output_path = r"d:\Work\The Conscious Coaching Factory\scratch\code_obsolete_list.txt"
with open(output_path, 'w', encoding='utf-8') as out_file:
    out_file.write(f"Active Code Obsolete Audit (Found {len(code_obsolete_files)} files):\n")
    for path, reason in sorted(code_obsolete_files):
        out_file.write(f"  - {path} ({reason})\n")

print("Audit completed. Written to scratch/code_obsolete_list.txt")
