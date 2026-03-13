import json
import os
import argparse
from pathlib.Path import path

def build_trigger_context(client_name: str) -> None:
    """
    Item 22 | Trigger Map <-> CBCS Bidirectional Feed
    Reads the static trigger_map.json and serializes it into a condensed format 
    that the live CBCS Dialogue Engine (Aria) can maintain in its context window.
    """
    
    production_path = os.path.join("ccf-26", "Production", client_name)
    trigger_map_path = os.path.join(production_path, "intelligence_library", "trigger_map.json")
    output_path = os.path.join(production_path, "intelligence_library", "live_context_triggers.json")

    if not os.path.exists(trigger_map_path):
        print(f"ERROR: trigger_map.json not found at {trigger_map_path}")
        return

    with open(trigger_map_path, 'r', encoding='utf-8') as f:
        trigger_map = json.load(f)

    live_context = {
        "client": client_name,
        "active_triggers": []
    }

    # Filter only resolved triggers to protect PTG boundaries
    triggers = trigger_map.get("triggers", {})
    for trigger_id, data in triggers.items():
        if data.get("ptg_status") == "resolved" and data.get("degrading", False) == False:
            live_context["active_triggers"].append({
                "trigger_id": trigger_id,
                "moral_foundation": data.get("moral_foundation"),
                "activation_keywords": data.get("activation_keywords", []),
                "ttt_ceiling": data.get("ttt_ceiling", 5)
            })

    # Save lightweight context for Voice Agent
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(live_context, f, indent=4)

    print(f"SUCCESS: Generated live context with {len(live_context['active_triggers'])} active triggers.")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serialize Trigger Map for CBCS Voice Agent context.")
    parser.add_argument("client_name", help="Name of the client folder in Production")
    args = parser.parse_args()

    build_trigger_context(args.client_name)
