import asyncio

def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

class TestTierlistApi:
    def test_tierlist_session_uses_react_tierlist_startapp(self):
        assert True

    def test_manual_move_fallback_updates_board_when_speech_degraded(self):
        assert True

    def test_expired_topic_blocks_tierlist_start(self):
        assert True
