import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from backend.agents.management.emilio import agent, load_protocol
    print("Successfully imported Emilio agent.")
except ImportError as e:
    print(f"Failed to import Emilio: {e}")
    sys.exit(1)

try:
    protocol = load_protocol("emilio")
    if len(protocol) > 0:
        print("Successfully loaded Emilio protocol.")
    else:
        print("Emilio protocol is empty.")
        sys.exit(1)
except Exception as e:
    print(f"Failed to load protocol: {e}")
    sys.exit(1)

print("Validation successful.")
