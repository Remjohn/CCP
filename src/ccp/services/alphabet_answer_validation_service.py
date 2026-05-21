from src.ccp.models.reaction_alphabet_models import AlphabetChallengeRoundPrompt

class AlphabetAnswerValidationService:
    def evaluate(self, coach_id: str, prompt: AlphabetChallengeRoundPrompt, captured_phrase: str) -> str:
        if not captured_phrase:
            return "invalid"
            
        phrase = captured_phrase.lower()
        target_letter = prompt.letter.lower()
        
        # Exact match rule for testing/stubbing NIM
        if phrase.startswith(target_letter):
            return "valid"
            
        return "invalid"
