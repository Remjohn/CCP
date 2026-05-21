import os
import re
import shutil

mcda_path = r"d:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\MCDA_Audit_Text_Finetuning_Consolidated.md"
target_dir = r"d:\Work\The Conscious Coaching Factory\lab\LoRa Activation Steering and Embegging papers\Text fine-tuning"

primary_dir = os.path.join(target_dir, "1_Primary_CCV_Protocol")
archive_dir = os.path.join(target_dir, "9_Archived_Context")
unscored_dir = os.path.join(target_dir, "0_Unscored")

os.makedirs(primary_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)
os.makedirs(unscored_dir, exist_ok=True)

with open(mcda_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

paper_scores = []
current_title = ""

for line in lines:
    if line.startswith("### "):
        # e.g., "### 1. A Unified Study of LoRA Variants Taxonomy"
        parts = line.split(".", 1)
        if len(parts) > 1:
            current_title = parts[1].strip()
    elif current_title and "- **Score:**" in line:
        match = re.search(r"\*\*Score:\*\*\s*(\d+)", line)
        if match:
            score = int(match.group(1))
            clean_title = re.sub(r'[\\/*?:"<>|]', "", current_title)
            fuzzy_title = " ".join(clean_title.split()[:4]).lower()
            paper_scores.append((fuzzy_title, score))
        current_title = ""

print(f"Loaded {len(paper_scores)} scored papers from MCDA.")

def get_action(filename):
    lower_name = filename.lower()
    if "can good writing be generative" in lower_name:
        return primary_dir
    
    for title, score in paper_scores:
        if title in lower_name:
            if score > 80: return primary_dir
            else: return archive_dir
    return unscored_dir

moved_primary = 0
moved_archive = 0

for filename in os.listdir(target_dir):
    file_path = os.path.join(target_dir, filename)
    if os.path.isdir(file_path): continue
        
    if filename.endswith(".md") or filename.endswith(".pdf"):
        dest_folder = get_action(filename)
        shutil.move(file_path, os.path.join(dest_folder, filename))
        if dest_folder == primary_dir: moved_primary += 1
        elif dest_folder == archive_dir: moved_archive += 1

print(f"Moved {moved_primary} files to Primary CCV Protocol.")
print(f"Moved {moved_archive} files to Archived Context.")
