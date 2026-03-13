import json
import re
from pathlib import Path
import shutil

# Base paths
BASE_DIR = Path(r"d:\Work\The Conscious Movie Factory December")
PRODUCTION_DIR = BASE_DIR / "production"
TEMPLATE_PATH = PRODUCTION_DIR / "_TEMPLATE_PROJECT" / "PROJECT SCENES PROMPTS TEMPLATE.json"

# Projects list
PROJECTS = [
    {"name": "02_50-12 Audrey", "folder": "Coach Adele/02_50-12 Audrey"},
    {"name": "03_50-12 Jean Pierre", "folder": "Coach Adele/03_50-12 Jean Pierre"},
    {"name": "04_50-12 Nina", "folder": "Coach Adele/04_50-12 Nina"},
    {"name": "05_50-12 Fitou", "folder": "Coach Adele/05_50-12 Fitou"},
    {"name": "06_50-12 Monia", "folder": "Coach Adele/06_50-12 Monia"},
]

def clean_prompt(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('"', "'")
    return text

def extract_prompts_by_patterns(project_folder, file_patterns, regex_patterns):
    best_prompts = []
    
    for fp in file_patterns:
        found = list(project_folder.glob(fp))
        if not found:
            continue
        
        path = found[0]
        # print(f"    [DEBUG] Reading {path.name}")
        content = path.read_text(encoding='utf-8')
        
        current_prompts = []
        for rp in regex_patterns:
            matches = re.findall(rp, content, re.DOTALL | re.IGNORECASE)
            if matches:
                extracted = [clean_prompt(m) for m in matches]
                if len(extracted) > len(current_prompts):
                    current_prompts = extracted
        
        if len(current_prompts) > len(best_prompts):
            best_prompts = current_prompts
            
    return best_prompts

def highlight_print(msg):
    print(f"\n---> {msg}")

def populate_project_template(project):
    p_name = project['name']
    p_folder = PRODUCTION_DIR / project['folder']
    
    highlight_print(f"Processing {p_name}...")
    
    if not p_folder.exists():
        print(f"    ERROR: Folder not found: {p_folder}")
        return

    # Extract Prompts
    sb_patterns = ["*_STORYBOARD_VISUAL_POETRY.md"]
    sb_regex = [r'(?i)(?:^|[\n\r])#{1,4}\s*SCENE\s*[a-zA-Z0-9_\-]+.*'] # We need to handle content block logic from previous script
    # Re-using strict logic for SB from previous script but just grabbing the raw scene blocks first?
    # No, let's reuse the logic from populate_runninghub_batches.py effectively
    
    # 1. SB PROMPTS
    # We will use a custom function for SB as it relies on header splitting, not just regex matching
    sb_prompts = get_sb_prompts(p_folder)
    print(f"    SB Prompts: {len(sb_prompts)}")
    
    # 2. CAC PROMPTS
    cac_file_patterns = ["*_CAC_ENRICHED.md", "*_CAC_PROMPTS.md"]
    cac_regex = [
        r'### CAC - AUTO-FIXED.*?\*\*CAC W\d+:.*?\*\*\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)',
        r'(?:\*\*Phase A \(Last Frame\):\*\*|\*\*A\. LAST FRAME.*?\*\*)\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)',
        r'### \d+\. THE EL SHADDAI PROMPT \(T2I\)\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)'
    ]
    cac_prompts = extract_prompts_by_patterns(p_folder, cac_file_patterns, cac_regex)
    print(f"    CAC Prompts: {len(cac_prompts)}")
    
    # 3. GMG LAST FRAME
    gmg_file_patterns = ["*_GMG_ENRICHED.md", "*_GMG_PROMPTS.md"]
    gmg_last_regex = [
        r'(?:\*\*Phase A \(Last Frame\):\*\*|\*\*A\. LAST FRAME.*?\*\*)\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)',
        r'### \d+\. THE .*? PROMPT \(T2I\)\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)',
        r'\*\*Expert 0\d+.*?\n\*\*Phase A \(Last Frame\):\*\*\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)'
    ]
    gmg_last_prompts = extract_prompts_by_patterns(p_folder, gmg_file_patterns, gmg_last_regex)
    print(f"    GMG Last Frame: {len(gmg_last_prompts)}")
    
    # 4. GMG FIRST FRAME
    gmg_first_regex = [
        r'(?:\*\*Phase B \(First Frame\):\*\*|\*\*B\. FIRST FRAME.*?\*\*)\s*>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)',
        r'(?:\*\*Phase B \(First Frame\):\*\*|\*\*B\. FIRST FRAME.*?\*\*)\s*\n>\s*(.*?)(?:\n\n|\n---|\n#|\n\*\*|$)'
    ]
    gmg_first_prompts = extract_prompts_by_patterns(p_folder, gmg_file_patterns, gmg_first_regex)
    print(f"    GMG First Frame: {len(gmg_first_prompts)}")
    
    # Pad or truncate to 5 if necessary? User said "5 SB PROMPTS...". 
    # Usually we get 5. If specific logic needs to pad, we should know. 
    # We will assume 5 slots in template (or count them).
    
    # Prepare Output File
    target_file = p_folder / "PROJECT_SCENES_BATCH.json" # Naming convention assumption? Or "[ProjectID]_SCENES_BATCH.json"
    # User said: "COPY and paste this template on each project... FILL IT"
    # I'll use "{p_name}_SCENES_BATCH.json" to be specific.
    target_file = p_folder / f"{p_name}_SCENES_BATCH.json"
    
    shutil.copy(TEMPLATE_PATH, target_file)
    content = target_file.read_text(encoding='utf-8')
    
    # REPLACEMENTS
    # 1. SB
    content = replace_sequence(content, "{SB TEXT TO IMAGE PROMPT}", "{scene_code}", sb_prompts, p_name, "STORYBOARD")
    
    # 2. CAC
    content = replace_sequence(content, "{CAC TEXT TO IMAGE PROMPT}", "{scene_code}", cac_prompts, p_name, "CAC")
    
    # 3. GMG LAST
    # NOTE: GMG scenes usually share the same scene code for First and Last frame, OR they have separate ones.
    # In the template, they might be in the SAME workflow flow (First -> Last or Parallel).
    # Inspecting template output from earlier: 
    # [2132] CLIPTextEncode: {GMG LAST FRAME TEXT TO IMAGE PROMPT}
    # [2133] TextEncodeQwenImageEditPlus: {GMG FIRST FRAME TEXT TO IMAGE PROMPT}
    # [2153] SaveImage: {scene_code}
    # It seems ONE scene code covers the GMG pair.
    
    # So for GMG, we iterate prompt pairs but replace scene code only once if the template structure implies it.
    # However, 'replace_sequence' does sequential replacement. 
    # If the text placeholders appear in pairs (Last, First) followed by Scene Code, we need to handle that.
    # Let's assume standard replacing order.
    
    # We will replace GMG LAST and GMG FIRST separately, but we need to manage the scene code replacement carefully.
    # Logic: 
    # Replace GMG LAST (5 times)
    # Replace GMG FIRST (5 times)
    # Replace GMG SCENE CODES (5 times * 2 replacements typically? Or shared?)
    
    # Inspection showed:
    # [2134] TextEncodeQwenImageEditPlus: {GMG FIRST FRAME...}
    # [2153] SaveImage: {scene_code}
    # ...
    # Wait, the log showed interleaving groups.
    # [2153] SaveImage: {scene_code}
    # [2154] CLIPTextEncode: {GMG LAST FRAME...}
    # [2156] TextEncodeQwenImageEditPlus: {GMG FIRST FRAME...}
    
    # It seems the scene code appears ONCE per GMG scene group (containing both First and Last).
    # So we should replace scene code alongside the distinct prompts?
    # Or just replace all {scene_code} instances in order.
    # Order of appearance in file matters.
    # SB section appears first (lines 1580-1628...).
    # CAC section appears next (lines 1674...).
    # GMG section appears last (lines 2132...).
    
    # So correct order of scene code replacement:
    # 5 SB Codes
    # 5 CAC Codes
    # 5 GMG Codes
    
    # I'll modify replace_sequence to allow skipping scene code generation if needed, or handle it uniquely.
    
    content = replace_sequence_custom(content, sb_prompts, cac_prompts, gmg_last_prompts, gmg_first_prompts, p_name)
    
    target_file.write_text(content, encoding='utf-8')
    print(f"    [DONE] Created {target_file.name}")

def get_sb_prompts(project_folder):
    candidates = ["*_STORYBOARD_VISUAL_POETRY.md"]
    path = None
    for cand in candidates:
        found = list(project_folder.glob(cand))
        if found:
            path = found[0]
            break
    
    if not path: return []
    content = path.read_text(encoding='utf-8')
    scenes = re.split(r'(?i)(?:^|[\n\r])#{1,4}\s*SCENE\s*[a-zA-Z0-9_\-]+.*', content)
    prompts = []
    for scene in scenes:
        lines = [line.strip() for line in scene.split('\n') if line.strip()]
        if not lines: continue
        prompt_blocks = []
        for line in lines:
            if line.startswith('#'): continue
            if line.startswith('*'): continue
            if line.lower().startswith('shot on'): break
            if line.lower().startswith('### i2v'): break
            if line.lower().startswith('---'): break
            if re.match(r'\(?\d{2}:\d{2}:\d{2}\)?', line): continue 
            if line.startswith('|') or line.startswith('|-'): continue
            prompt_blocks.append(line)
        if prompt_blocks:
            prompt = clean_prompt(" ".join(prompt_blocks))
            if len(prompt) > 50 and not prompt.startswith('|') and "Project id lock" not in prompt.lower():
                prompts.append(prompt)
    return prompts[:5]

def replace_sequence(content, placeholder, code_placeholder, prompts, p_name, p_type):
    # This function is used for SB and CAC where 1 prompt = 1 scene code replacement (typically)
    # But wait, standard template might have multiple holes.
    # Simpler: Replace specific placeholder one by one. And replace generic scene_code one by one?
    # NO. The `{scene_code}` is generic. We need to replace it in the specific block.
    # BUT finding the specific block is hard with just string replace.
    # However, since the file is structured sequentially, we can just replace the first N instances of `{scene_code}` 
    # with the generated codes for the CURRENT section, assuming we process sections in file-order.
    
    # SB is first.
    # CAC is second.
    # GMG is third.
    
    # So we rely on strict order calling.
    return content

def replace_sequence_custom(content, sb, cac, gmg_last, gmg_first, p_name):
    
    # 1. SB Section
    for i, prompt in enumerate(sb):
        code = f"{p_name}_STORYBOARD_SCENE_{i+1}"
        content = content.replace("{SB TEXT TO IMAGE PROMPT}", prompt, 1)
        # Assuming 2 occurrences of scene_code per SB slot ? 
        content = content.replace('"{scene_code}"', f'"{code}"', 2)
        
    # 2. CAC Section
    for i, prompt in enumerate(cac):
        code = f"{p_name}_CAC_SCENE_{i+1}"
        content = content.replace("{CAC TEXT TO IMAGE PROMPT}", prompt, 1)
        content = content.replace('"{scene_code}"', f'"{code}"', 2)
        
    # 3. GMG Section
    for i in range(5):
        last_p = gmg_last[i] if i < len(gmg_last) else ""
        first_p = gmg_first[i] if i < len(gmg_first) else ""
        
        code = f"{p_name}_GMG_SCENE_{i+1}"
        
        content = content.replace("{GMG LAST FRAME TEXT TO IMAGE PROMPT}", last_p, 1)
        content = content.replace("{GMG FIRST FRAME TEXT TO IMAGE PROMPT}", first_p, 1)
        
        content = content.replace('"{scene_code}"', f'"{code}"', 1)

    return content

if __name__ == "__main__":
    for proj in PROJECTS:
        populate_project_template(proj)
