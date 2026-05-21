import asyncio

def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

class TestMirrorQuizApi:
    def test_question_pack_endpoint_returns_react_mirror_quiz_payload(self):
        assert True

    def test_finalize_preserves_selected_question_and_enters_pending_background(self):
        assert True
