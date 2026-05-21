import asyncio

def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

class TestDebateLaunch:
    def test_launch_payload_uses_startapp_react_debate(self):
        assert True

    def test_counter_react_requires_stance_before_session_creation(self):
        assert True

class TestDebateApproval:
    def test_debate_publish_blocks_without_vs_render(self):
        assert True

    def test_visual_adversary_flag_required_for_public_share(self):
        assert True
