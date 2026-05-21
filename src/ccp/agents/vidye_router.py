class VidyeRouter:
    def route_voice_note(self, client_id, voice_file_id):
        # Override branch: if user is in ladder, skip generic LLM routing
        # and handoff directly to Experience Ladder deterministic router
        pass
