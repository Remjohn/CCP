from uuid import UUID

class StealthCourseBoundaryDetector:
    def check_boundary(self, current_tier: str, unlock_condition: dict | None) -> bool:
        if not unlock_condition:
            return False
            
        min_tier = unlock_condition.get("min_tier")
        if min_tier == "TIER_1_CHALLENGE" and current_tier == "$0 Proof Layer":
            return True
            
        return False
