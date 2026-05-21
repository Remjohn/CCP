from datetime import datetime
from src.ccp.models.reaction_alphabet_models import AlphabetTimingVerificationPayload, TimingVerificationStatus

class AlphabetTimingVerifier:
    def verify(self, payload: AlphabetTimingVerificationPayload) -> AlphabetTimingVerificationPayload:
        suspicious_indexes = []
        status = TimingVerificationStatus.VERIFIED

        for i, rr in enumerate(payload.round_results):
            timing = rr.timing
            
            # Phase2-M07 check: Never use server request receive time to override
            # Check internal consistency of monotonic clock
            if timing.answer_detected_at_client_ms is not None:
                expected_elapsed = timing.answer_detected_at_client_ms - timing.letter_revealed_at_client_ms
                if timing.elapsed_ms is not None and abs(expected_elapsed - timing.elapsed_ms) > 10:
                    suspicious_indexes.append(i)
                    
            if timing.client_clock_source == "date.now_fallback":
                if status == TimingVerificationStatus.VERIFIED:
                    status = TimingVerificationStatus.VERIFIED_WITH_DRIFT
                    
            # Check coarse wall clock tampering
            if timing.client_epoch_answered_at_ms is not None:
                wall_diff = timing.client_epoch_answered_at_ms - timing.client_epoch_revealed_at_ms
                if timing.elapsed_ms is not None and wall_diff < timing.elapsed_ms - 1000:
                    suspicious_indexes.append(i)

        if suspicious_indexes:
            status = TimingVerificationStatus.SUSPICIOUS

        payload.verification_status = status
        payload.suspicious_round_indexes = suspicious_indexes
        return payload
