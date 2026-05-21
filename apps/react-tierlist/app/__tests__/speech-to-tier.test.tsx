import { interpretSpeechCommand } from '../lib/speech-to-tier';

describe('speech-to-tier', () => {
    it('maps [element] goes in S Tier to the correct item and tier', () => {
        const items = [{ id: "1", name: "Apple" }];
        const result = interpretSpeechCommand("Apple goes in S Tier", items);
        expect(result?.target_tier).toBe("S");
        expect(result?.item_id).toBe("1");
    });

    it('rejects low-confidence ambiguous commands without mutating the board', () => {
        const items = [{ id: "1", name: "Apple" }];
        const result = interpretSpeechCommand("Banana in D row", items);
        expect(result).toBeNull();
    });
});
