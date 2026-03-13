import re
from pathlib import Path
import yaml

MANDATORY_INPUTS = {
    "structural_congruence_point",
    "voice_dna_spr",
    "emotional_dna",
    "negative_space",
    "audience_tribal_terms",
    "authentication_certificate",
    "archetype_metadata",
    "context_premise_summary"
}

def validate_prompt(filepath: Path) -> list:
    violations = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Check YAML Frontmatter
    parts = content.split("---")
    if len(parts) < 3:
        return ["Missing or invalid YAML frontmatter"]
        
    frontmatter = parts[1]
    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError:
        return ["Invalid YAML syntax in frontmatter"]
        
    # 2. Check Mandatory Inputs
    inputs = metadata.get("inputs", [])
    input_names = set(i.split(" ")[0] for i in inputs) if isinstance(inputs, list) else set()
    
    missing_inputs = MANDATORY_INPUTS - input_names
    if missing_inputs:
        violations.append(f"Missing mandatory inputs: {missing_inputs}")
        
    # 3. Check Priming Protocol
    main_body = "---".join(parts[2:])
    if "Layer 1" not in main_body or "Layer 2" not in main_body or "Layer 3" not in main_body:
        violations.append("Missing 3-Layer Priming Protocol")
        
    # 4. Check Loading Sequence (Negative Space must be first)
    load_section_match = re.search(r"### Load 1:(.*?)(?:\n### Load 2:|\Z)", main_body, re.DOTALL)
    if not load_section_match or "negative_space" not in load_section_match.group(1).lower():
        violations.append("Negative Space is not loaded first (in Load 1)")
        
    # 5. Check Role Assignments (Doctrine Violation)
    role_pattern = re.compile(r"you are a[n]?\s+(?!executing)", re.IGNORECASE)
    if role_pattern.search(main_body):
        violations.append("Found forbidden role assignment ('You are a...')")
        
    # 6. Check Legacy Variables
    if "{content_idea}" in main_body or "{Conscious_Soul_Values}" in main_body:
        violations.append("Found legacy variables ({content_idea} or {Conscious_Soul_Values})")
        
    # 7. Check Post-Hoc Validation Checklists (Doctrine Violation)
    post_hoc_pattern = re.compile(r"\?\n- \[ \]") # Looking for questions immediately followed by a checklist
    if post_hoc_pattern.search(main_body):
        violations.append("Found forbidden post-hoc validation checklist question")
        
    return violations

def run_validation(directory: str):
    base_path = Path(directory)
    if not base_path.exists():
        print(f"Directory not found: {directory}")
        return
        
    print(f"Validating SKILL.md files in {directory}...")
    checked = 0
    failed = 0
    
    for skill_file in base_path.rglob("SKILL.md"):
        # Skip templates
        if "_template" in str(skill_file):
            continue
            
        checked += 1
        violations = validate_prompt(skill_file)
        
        if violations:
            failed += 1
            print(f"\n❌ FAILED: {skill_file.relative_to(base_path)}")
            for v in violations:
                print(f"   - {v}")
        else:
            print(f"✅ PASSED: {skill_file.relative_to(base_path)}")
            
    print(f"\nSummary: {checked} files checked, {checked - failed} passed, {failed} failed.")

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Validate V3 Trigger-First SKILL.md prompts")
    parser.add_argument("directory", nargs="?", default="d:/Work/The Conscious Coaching Factory/skills/ccf/content/archetypes", help="Directory to scan")
    args = parser.parse_args()
    
    run_validation(args.directory)
