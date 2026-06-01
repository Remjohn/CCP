import re
import os

def extract_questions(file_path):
    questions = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Match lines starting with "Number. " (e.g. "1. What is...")
            match = re.match(r"^(\d+)\.\s+(.*)$", line)
            if match:
                q_num = int(match.group(1))
                q_text = match.group(2)
                questions[q_num] = q_text
    return questions

def update_answers_file(answers_path, questions):
    if not os.path.exists(answers_path):
        print(f"Error: {answers_path} not found.")
        return
        
    with open(answers_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # We want to find each section starting with "### [Number]. [Heading]"
    # and insert "**Question:** [Question Text]\n\n" right after it.
    # To do this safely and cleanly, we can split the file by "### "
    parts = content.split("\n### ")
    new_parts = [parts[0]] # Keep the header
    
    for part in parts[1:]:
        # Extract the number from the heading (e.g. "1. Data Contract...")
        match = re.match(r"^(\d+)\.\s+(.*?)\n(.*)$", part, re.DOTALL)
        if match:
            q_num = int(match.group(1))
            heading = match.group(2).strip()
            rest = match.group(3)
            
            q_text = questions.get(q_num, "")
            if not q_text:
                print(f"Warning: Question {q_num} not found in source questions list.")
                
            # Construct the new part
            new_part = f"{q_num}. {heading}\n**Question:** {q_text}\n\n{rest.strip()}"
            new_parts.append(new_part)
        else:
            new_parts.append(part)
            
    updated_content = "\n### ".join(new_parts)
    
    with open(answers_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"Successfully updated {answers_path} with question texts.")

# Paths
workspace_dir = r"d:\Work\The Conscious Coaching Factory"
audit_questions_path = os.path.join(workspace_dir, "docs", "architecture", "May 2026 UPDATES", "Architectural_Audit_Trigger_First_Vision_Visual_Engines.md")
harness_questions_path = os.path.join(workspace_dir, "docs", "architecture", "May 2026 UPDATES", "CCP_Actual_Harness_Extraction_Philosophy_And_60_Questions.md")

audit_answers_path = os.path.join(workspace_dir, "docs", "architecture", "May 2026 UPDATES", "Architectural_Audit_60_Answers.md")
harness_answers_path = os.path.join(workspace_dir, "docs", "architecture", "May 2026 UPDATES", "Actual_Harness_60_Answers.md")

# Process Audit Questions & Answers
audit_questions = extract_questions(audit_questions_path)
print(f"Extracted {len(audit_questions)} questions from Audit file.")
update_answers_file(audit_answers_path, audit_questions)

# Process Harness Questions & Answers
harness_questions = extract_questions(harness_questions_path)
print(f"Extracted {len(harness_questions)} questions from Harness file.")
update_answers_file(harness_answers_path, harness_questions)
