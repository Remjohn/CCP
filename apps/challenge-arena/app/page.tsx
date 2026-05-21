import React from 'react';
import SessionHeader from './components/session-header';
import DailyRouteCard from './components/daily-route-card';
import ProgressionRail from './components/progression-rail';

export default function Page() {
  return (
    <main className="container">
      <SessionHeader />
      <div className="layout-content">
        <ProgressionRail />
        <DailyRouteCard />
      </div>
    </main>
  );
}
