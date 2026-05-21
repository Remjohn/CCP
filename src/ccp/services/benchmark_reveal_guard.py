from src.ccp.models.onboarding_models import AnonymousOnboardingSession

class BenchmarkRevealGuard:
    @staticmethod
    def assert_reveal_completed(session: AnonymousOnboardingSession) -> bool:
        if not session.benchmark_revealed_at:
            raise ValueError("M-07 Violation: Benchmark must be revealed before this transition.")
        return True
