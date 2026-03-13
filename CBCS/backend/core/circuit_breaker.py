from typing import Dict

class CostCircuitBreaker:
    def __init__(self):
        self.user_costs: Dict[str, float] = {}
        self.limit_usd = 4.00

    def track_cost(self, user_id: str, cost_usd: float):
        """
        Adds cost to the user's cumulative total.
        """
        if user_id not in self.user_costs:
            self.user_costs[user_id] = 0.0
        self.user_costs[user_id] += cost_usd

    def should_downgrade(self, user_id: str) -> bool:
        """
        Returns True if the user has exceeded the budget limit.
        """
        current_cost = self.user_costs.get(user_id, 0.0)
        return current_cost > self.limit_usd

    def reset_cost(self, user_id: str):
        """
        Resets the cost for a user (e.g., at the start of a new billing cycle).
        """
        self.user_costs[user_id] = 0.0

# Global Instance
circuit_breaker = CostCircuitBreaker()
