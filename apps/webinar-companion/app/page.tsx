'use client';

import React, { useState } from 'react';
import VideoStage from './components/video-stage';
import LowerThirdPrompt from './components/lower-third-prompt';
import RightDrawerPrompt from './components/right-drawer-prompt';
import ReplayTimeline from './components/replay-timeline';
import RepSlideScorecard from './components/rep-slide-scorecard';
import DownloadablesPanel from './components/downloadables-panel';

export default function Page() {
  const [activePrompt, setActivePrompt] = useState(null);
  const [activeScorecard, setActiveScorecard] = useState(null);

  return (
    <main className="container">
      <VideoStage />
      
      {activePrompt === 'lower-third' && <LowerThirdPrompt onClose={() => setActivePrompt(null)} />}
      {activePrompt === 'right-drawer' && <RightDrawerPrompt onClose={() => setActivePrompt(null)} />}
      
      <ReplayTimeline />
      
      {activeScorecard && <RepSlideScorecard data={activeScorecard} />}
      
      <DownloadablesPanel />
    </main>
  );
}
