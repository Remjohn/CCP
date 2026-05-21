import os
import re
import json

ARCH_DIR = r"d:\Work\The Conscious Coaching Factory\docs\architecture"
SERVICES_DIR = r"d:\Work\The Conscious Coaching Factory\src\ccp\services"
PIPELINES_DIR = r"d:\Work\The Conscious Coaching Factory\src\ccp\pipelines"
TESTS_DIR = r"d:\Work\The Conscious Coaching Factory\tests"

def parse_spec_file(filepath):
    filename = os.path.basename(filepath)
    # Extract clean Spec ID prefix
    prefix_match = re.match(r'^(FR-CA11-\d+|FR-CBCS-\d+|FR-VIS-\d+|FR-COM-\d+|FR0[A-E]|FR\d+|FR_CBCS_\d+|FR_GA)', filename, re.IGNORECASE)
    if prefix_match:
        spec_id = prefix_match.group(1).upper()
        # Standardize separators
        spec_id = spec_id.replace('_', '-')
    else:
        spec_id = filename.replace('.md', '')

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Look for DEP-IDs
    dep_ids = re.findall(r'DEP-[A-Z]+-\d+', content)
    dep_ids = list(set(dep_ids))

    # Look for produced DEP-ID
    produces = []
    proposed_matches = re.findall(r'DEP-[A-Z]+-\d+\s+PROPOSED', content)
    for p in proposed_matches:
        dep = p.split()[0]
        if dep not in produces:
            produces.append(dep)

    # In Section 5: Primary Output Schema
    sec5_match = re.search(r'## 5\.\s+Primary Output Schema.*?(?:## 6|$)', content, re.DOTALL | re.IGNORECASE)
    if sec5_match:
        sec5_content = sec5_match.group(0)
        sec5_deps = re.findall(r'DEP-[A-Z]+-\d+', sec5_content)
        for dep in sec5_deps:
            if dep not in produces:
                produces.append(dep)

    # In Section 3: Context for Development
    consumes = []
    sec3_match = re.search(r'## 3\.\s+Context for Development.*?(?:## 4|$)', content, re.DOTALL | re.IGNORECASE)
    if sec3_match:
        sec3_content = sec3_match.group(0)
        # Scan table lines
        lines = sec3_content.split('\n')
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    dep_match = re.findall(r'DEP-[A-Z]+-\d+', parts[1])
                    role = parts[3].upper() if len(parts) > 3 else ""
                    if dep_match:
                        dep = dep_match[0]
                        if "SOURCE" in role or "INPUT" in role or "CONSUME" in role:
                            if dep not in consumes:
                                consumes.append(dep)
                        elif "PRODUCE" in role or "OUTPUT" in role or "WRITE" in role:
                            if dep not in produces:
                                produces.append(dep)

    # Fallback scan of context
    for dep in dep_ids:
        if dep not in produces and dep not in consumes:
            pattern = re.compile(rf'\|\s*`?{re.escape(dep)}`?\s*\|.*?(SOURCE|INPUT|CONSUME|TRIGGER)', re.IGNORECASE)
            if pattern.search(content):
                consumes.append(dep)
            pattern_prod = re.compile(rf'\|\s*`?{re.escape(dep)}`?\s*\|.*?(PRODUCE|OUTPUT|WRITE|TARGET|CREATES)', re.IGNORECASE)
            if pattern_prod.search(content):
                produces.append(dep)

    # Search for files created or modified
    skill_impl = []
    skill_matches = re.findall(r'Skill Implementation:\s*`?([\w\.\/\-\\]+)`?', content, re.IGNORECASE)
    for sm in skill_matches:
        base = os.path.basename(sm)
        if base not in skill_impl:
            skill_impl.append(base)
            
    produces = [p for p in produces if p not in consumes]
    
    return {
        "spec_id": spec_id,
        "filename": filename,
        "produces": list(set(produces)),
        "consumes": list(set(consumes)),
        "skills": skill_impl,
        "content_length": len(content)
    }

def scan_all_specs():
    specs = []
    for f in os.listdir(ARCH_DIR):
        # Filter out reports and documentation
        if f.endswith('.md') and not any(term in f for term in [
            'Audit_Report', 'Stress_Test', 'Commercial_Layer', 'SPEC_REWRITE_BRIEFING', 
            'april_updates', 'cbar_audits', 'spec updates'
        ]):
            filepath = os.path.join(ARCH_DIR, f)
            specs.append(parse_spec_file(filepath))
    return specs

def check_build_and_test_status(specs):
    # Cache content of all service files
    service_contents = {}
    if os.path.exists(SERVICES_DIR):
        for s in os.listdir(SERVICES_DIR):
            if s.endswith('.py'):
                try:
                    with open(os.path.join(SERVICES_DIR, s), 'r', encoding='utf-8', errors='ignore') as f:
                        service_contents[s] = f.read()
                except Exception as e:
                    pass

    # Cache pipeline files
    pipeline_contents = {}
    if os.path.exists(PIPELINES_DIR):
        for p in os.listdir(PIPELINES_DIR):
            if p.endswith('.py'):
                try:
                    with open(os.path.join(PIPELINES_DIR, p), 'r', encoding='utf-8', errors='ignore') as f:
                        pipeline_contents[p] = f.read()
                except Exception as e:
                    pass

    # Cache tests
    test_contents = {}
    for sub in ["unit", "integration"]:
        sub_dir = os.path.join(TESTS_DIR, sub)
        if os.path.exists(sub_dir):
            for t in os.listdir(sub_dir):
                if t.endswith('.py'):
                    try:
                        with open(os.path.join(sub_dir, t), 'r', encoding='utf-8', errors='ignore') as f:
                            test_contents[os.path.join("tests", sub, t)] = f.read()
                    except Exception as e:
                        pass

    for spec in specs:
        spec_id = spec["spec_id"]
        
        # Determine build status
        build_status = "NOT STARTED"
        matching_files = []
        
        # Match by explicit Skill Implementation
        for skill in spec["skills"]:
            if skill in service_contents:
                matching_files.append(os.path.join("src/ccp/services", skill))
            elif skill in pipeline_contents:
                matching_files.append(os.path.join("src/ccp/pipelines", skill))

        # Match by searching spec_id (e.g. "FR-CA11-01" or "FR1") inside file contents
        clean_id = spec_id.lower().replace('-', '_')
        # Also clean the id to standard string representations
        search_terms = [spec_id, spec_id.replace('-', '_'), spec_id.lower(), spec_id.lower().replace('-', '_')]
        
        for s, s_content in service_contents.items():
            if any(term in s_content for term in search_terms) or clean_id in s.lower():
                matching_files.append(os.path.join("src/ccp/services", s))
                
        for p, p_content in pipeline_contents.items():
            if any(term in p_content for term in search_terms) or clean_id in p.lower():
                matching_files.append(os.path.join("src/ccp/pipelines", p))
                
        if matching_files:
            build_status = "IMPLEMENTED"
            spec["impl_files"] = list(set(matching_files))
        else:
            spec["impl_files"] = []
            
        # Check tests
        test_status = "NO TESTS"
        matching_tests = []
        
        # Search for spec_id in test contents or filename
        for t_path, t_content in test_contents.items():
            t_filename = os.path.basename(t_path)
            # Match by searching content or fuzzy filename match
            if any(term in t_content for term in search_terms) or clean_id in t_filename.lower():
                matching_tests.append(t_path)
                
        # Fallback numeric patterns
        if not matching_tests:
            num_part = ""
            num_match = re.findall(r'\d+', spec_id)
            if num_match:
                num_part = num_match[-1]
            test_patterns = []
            if spec_id.startswith('FR-CA11-'):
                test_patterns.append(f"test_ca11_fr{num_part}")
            elif spec_id.startswith('FR-CBCS-'):
                test_patterns.append(f"test_cbcs{num_part}")
            elif spec_id.startswith('FR-VIS-'):
                test_patterns.append(f"test_vis{num_part}")
                test_patterns.append(f"test_cpsc_fr{num_part}")
            elif spec_id.startswith('FR-COM-'):
                test_patterns.append(f"test_com{num_part}")
            elif spec_id.startswith('FR0'):
                char = spec_id[-1].lower()
                test_patterns.append(f"test_fr0{char}")
            elif spec_id.startswith('FR'):
                test_patterns.append(f"test_fr{num_part}")
                test_patterns.append(f"test_cpsc_fr{num_part}")
                test_patterns.append(f"test_era3_fr{num_part}")

            for t_path in test_contents.keys():
                t_filename = os.path.basename(t_path)
                for pat in test_patterns:
                    if pat in t_filename.lower():
                        matching_tests.append(t_path)
                        
        if matching_tests:
            test_status = "TESTS FOUND"
            spec["test_files"] = list(set(matching_tests))
        else:
            spec["test_files"] = []
            
        spec["build_status"] = build_status
        spec["test_status"] = test_status

    return specs

if __name__ == "__main__":
    specs = scan_all_specs()
    specs = check_build_and_test_status(specs)
    
    with open("scratch_specs_parsed.json", "w") as f:
        json.dump(specs, f, indent=2)
        
    print(f"Parsed {len(specs)} specs.")
    
    # Group by category
    categories = {}
    for spec in specs:
        id_prefix = spec["spec_id"].split('-')[0]
        if id_prefix.startswith('FR0'):
            cat = "Genesis (CA-0)"
        elif id_prefix.startswith('FR-CBCS'):
            cat = "Relationship (CA-5B)"
        elif id_prefix.startswith('FR-CA11'):
            cat = "Workspace/Studio (CA-11)"
        elif id_prefix.startswith('FR-VIS'):
            cat = "Visual Engine (CVE)"
        elif id_prefix.startswith('FR-COM'):
            cat = "Billing/Admin (COM)"
        else:
            try:
                num = int(re.findall(r'\d+', spec["spec_id"])[0])
                if num <= 13:
                    cat = "Identity & Voice (CA-1)"
                elif num <= 17:
                    cat = "CRAL Research (CA-3)"
                elif num <= 23:
                    cat = "Psych Routing (CA-2)"
                elif num <= 26:
                    cat = "Weekly/Governance (CA-4)"
                elif num <= 32:
                    cat = "Coaching Client (CA-5)"
                elif num <= 36:
                    cat = "Webinar System (CA-6)"
                elif num <= 41:
                    cat = "Cross-System/Memory (CA-7)"
                elif num <= 50:
                    cat = "Performance/Tenant (CA-8)"
                elif num <= 60:
                    cat = "CPSC Sales Funnel (CA-9)"
                else:
                    cat = "Other"
            except:
                cat = "Other"
                
        categories.setdefault(cat, []).append(spec["spec_id"])
        
    # Print status statistics
    total_implemented = sum(1 for s in specs if s["build_status"] == "IMPLEMENTED")
    total_tested = sum(1 for s in specs if s["test_status"] == "TESTS FOUND")
    print(f"Implementation status: {total_implemented}/{len(specs)} specs mapped to build files.")
    print(f"Testing status: {total_tested}/{len(specs)} specs mapped to test files.")
    
    for cat, list_ids in sorted(categories.items()):
        print(f"{cat}: {len(list_ids)} specs ({', '.join(sorted(list_ids[:5]))}... total {len(list_ids)})")

