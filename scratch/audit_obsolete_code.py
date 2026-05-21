import os
import re

SERVICES_DIR = r"d:\Work\The Conscious Coaching Factory\src\ccp\services"
API_DIR = r"d:\Work\The Conscious Coaching Factory\src\ccp\api"

# Define the obsolete patterns in services and APIs based on PRD Modules:
# 1. Standalone Trivianar: trivianar_engine_service.py, interactive_trivianar, etc.
# 2. Canva / HTML Canvas: canvas_composition_service.py, canvas_api.py, canva-app
# 3. WebRTC Synchronous: webrtc, live_rooms, synchronous roleplay, live_cohost
# 4. Legacy Affiliate / Loud Referral: affiliate_service.py, referral_dashboard, advocate_ledger
# 5. External Web Checkout: checkout_service.py, web_portal
# 6. Static intake forms: intake_questionnaire, static_intake

obsolete_keywords = {
    "trivianar": "Trivianar Synchronous Engine (PRD-06 §500)",
    "canvas_composition": "Canva-Style HTML Canvas Builder (PRD-07 §1288)",
    "webrtc": "Live Synchronous WebRTC Roleplay (PRD-04 §1124)",
    "affiliate": "Loud Referral / Explicit Affiliate Systems (PRD-09 §1257)",
    "advocate_ledger": "Advocate Ledger & Whale Slider (PRD-01 §693)",
    "checkout": "External Web Checkout Portals (PRD-09 §1256)",
    "intake": "Static Form-Based Intake Services (PRD-05 §1158)"
}

obsolete_files = []

for root_dir in [SERVICES_DIR, API_DIR]:
    if not os.path.exists(root_dir):
        continue
    for f in os.listdir(root_dir):
        if not f.endswith('.py'):
            continue
        filepath = os.path.join(root_dir, f)
        
        # Check filename
        matched_kw = None
        for kw, desc in obsolete_keywords.items():
            if kw in f.lower():
                matched_kw = kw
                break
                
        # Also check content for obsolete warnings
        content = ""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                content = file_obj.read()
        except:
            pass
            
        if not matched_kw:
            for kw, desc in obsolete_keywords.items():
                if kw in content.lower():
                    # Check context to see if it actually implements it
                    if f"class {kw}" in content.lower() or f"def {kw}" in content.lower():
                        matched_kw = kw
                        break
                        
        if matched_kw:
            rel_path = os.path.relpath(filepath, r"d:\Work\The Conscious Coaching Factory")
            obsolete_files.append({
                "file": rel_path,
                "reason": obsolete_keywords[matched_kw],
                "has_shim": "shim" in content.lower() or "obsolete" in content.lower()
            })

print(f"Audit of Obsolete Files in Codebase (Total found: {len(obsolete_files)}):")
for item in obsolete_files:
    print(f"  - {item['file']}")
    print(f"    Reason: {item['reason']}")
    print(f"    Status: {'Marked as Shim/Obsolete in code' if item['has_shim'] else 'Active Legacy Code (NEEDS DEPRECATION/CLEANUP)'}")
