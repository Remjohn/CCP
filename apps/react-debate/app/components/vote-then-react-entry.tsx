import React from 'react';
import { VoteThenReactPrompt } from '../lib/types';

export default function VoteThenReactEntry({ prompt }: { prompt: VoteThenReactPrompt }) {
    return (
        <div>
            <p>{prompt.prompt_copy}</p>
            <a href={prompt.deep_link_url}>Record Counter-Take</a>
        </div>
    );
}
