import os

EXCLUDED_DIRS = {'.git', '.venv', 'node_modules', 'primitives', '.pytest_cache', '__pycache__', 'dist', '.system_generated'}
OBSOLETE_KEYWORDS = ['notion', 'trivianar', 'webrtc', 'canva']

obsolete_files = []

for root, dirs, files in os.walk(r"d:\Work\The Conscious Coaching Factory"):
    # Filter out excluded directories
    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
    
    for f in files:
        filepath = os.path.join(root, f)
        rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
        
        # Check if file name has obsolete keyword
        matched = False
        for kw in OBSOLETE_KEYWORDS:
            if kw in f.lower():
                obsolete_files.append((rel_path, f"Filename contains '{kw}'"))
                matched = True
                break
                
        if not matched and f.endswith(('.py', '.json', '.md', '.ts', '.tsx')):
            # Check content
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                    content = file_obj.read()
                for kw in OBSOLETE_KEYWORDS:
                    if kw in content.lower():
                        # We only list if it has a high correlation or if it is in Python/TS source code
                        if any(term in content.lower() for term in ['import ', 'class ', 'def ', 'function ']) or 'config' in f.lower() or 'test_' in f:
                            obsolete_files.append((rel_path, f"Content references '{kw}'"))
                            break
            except:
                pass

output_path = r"d:\Work\The Conscious Coaching Factory\scratch\obsolete_list_compiled.txt"
with open(output_path, 'w', encoding='utf-8') as out_file:
    out_file.write(f"Obsolete Files Audit (Found {len(obsolete_files)} files):\n")
    for path, reason in sorted(obsolete_files):
        out_file.write(f"  - {path} ({reason})\n")

print("Audit completed. Written to scratch/obsolete_list_compiled.txt")
