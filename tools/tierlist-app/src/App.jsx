import React, { useState, useEffect, useCallback } from 'react';
import ExcalidrawCanvas from './components/ExcalidrawCanvas';
import VideoOverlay from './components/VideoOverlay';
import sampleConfig from './data/sample-config.json';

/**
 * CCF Tier List & Rating Recording Studio
 *
 * Main layout:
 * - Full-screen Excalidraw canvas (tier list or rating scale)
 * - Floating centered video overlay (25-30% viewport)
 * - Top bar with controls
 * - Right sidebar with commentary/criteria
 */
export default function App() {
    const [config, setConfig] = useState(sampleConfig);
    const [videoVisible, setVideoVisible] = useState(false);
    const [sidebarVisible, setSidebarVisible] = useState(true);
    const [excalidrawAPI, setExcalidrawAPI] = useState(null);

    // Keyboard shortcuts
    useEffect(() => {
        function handleKeyDown(e) {
            // Ctrl+V = toggle video
            if (e.ctrlKey && e.key === 'v' && !e.shiftKey) {
                // Only if not inside an input/textarea
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                    setVideoVisible((v) => !v);
                }
            }
            // Ctrl+B = toggle sidebar
            if (e.ctrlKey && e.key === 'b') {
                e.preventDefault();
                setSidebarVisible((v) => !v);
            }
            // Space = play/pause video (when overlay visible)
            if (e.key === ' ' && videoVisible) {
                // Only if not in Excalidraw text edit
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA'
                    && !e.target.closest('.excalidraw')) {
                    e.preventDefault();
                }
            }
        }
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [videoVisible]);

    // Handle config file drop
    const handleDrop = useCallback((e) => {
        e.preventDefault();
        const file = e.dataTransfer?.files?.[0];
        if (file && file.name.endsWith('.json')) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                try {
                    const data = JSON.parse(ev.target.result);
                    setConfig(data);
                } catch (err) {
                    console.error('Invalid config JSON:', err);
                }
            };
            reader.readAsText(file);
        }
    }, []);

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
    }, []);

    const modeLabel = config.mode === 'tier-list' ? 'TIER LIST' : 'RATING';
    const tierKeys = ['S', 'A', 'B', 'C', 'D', 'F'];

    return (
        <div
            className="app-container"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
        >
            {/* ── Top Bar ────────────────────────────────── */}
            <header className="top-bar">
                <div className="top-bar__logo">
                    <div className="top-bar__logo-icon">🎯</div>
                    <span>CCF STUDIO</span>
                    <div className="mode-badge">
                        <span className="mode-badge__dot" />
                        {modeLabel}
                    </div>
                </div>

                <div className="top-bar__title">{config.title || 'Untitled'}</div>

                <div className="top-bar__controls">
                    <button
                        className={`btn ${videoVisible ? 'btn--danger' : 'btn--accent'}`}
                        onClick={() => setVideoVisible((v) => !v)}
                        title="Toggle video overlay (Ctrl+V)"
                    >
                        <span className="btn__icon">{videoVisible ? '⏹' : '▶'}</span>
                        {videoVisible ? 'Hide Video' : 'Show Video'}
                    </button>
                    <button
                        className="btn"
                        onClick={() => setSidebarVisible((v) => !v)}
                        title="Toggle sidebar (Ctrl+B)"
                    >
                        <span className="btn__icon">📋</span>
                        Notes
                    </button>
                </div>
            </header>

            {/* ── Canvas ─────────────────────────────────── */}
            <div
                className="canvas-area"
                style={{
                    marginRight: sidebarVisible ? 280 : 0,
                    transition: 'margin-right 0.3s ease',
                }}
            >
                <ExcalidrawCanvas
                    config={config}
                    excalidrawAPI={excalidrawAPI}
                    setExcalidrawAPI={setExcalidrawAPI}
                />
            </div>

            {/* ── Video Overlay ──────────────────────────── */}
            <VideoOverlay
                videoSrc={config.reaction_video}
                visible={videoVisible}
                onToggle={() => setVideoVisible(false)}
            />

            {/* ── Right Sidebar ──────────────────────────── */}
            <aside className={`sidebar ${!sidebarVisible ? 'sidebar--hidden' : ''}`}>
                <div className="sidebar__header">Recording Notes</div>
                <div className="sidebar__content">

                    {/* Tier Legend */}
                    {config.mode === 'tier-list' && config.tiers && (
                        <div className="sidebar__section animate-in">
                            <div className="sidebar__section-title">Tier Legend</div>
                            <div className="tier-legend">
                                {tierKeys.map((key) => {
                                    const tier = config.tiers[key];
                                    if (!tier) return null;
                                    return (
                                        <div key={key} className="tier-legend__item">
                                            <div
                                                className="tier-legend__swatch"
                                                style={{ background: tier.color }}
                                            />
                                            <span className="tier-legend__label">{key}</span>
                                            <span className="tier-legend__desc">{tier.label}</span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}

                    {/* Criteria */}
                    {config.criteria?.length > 0 && (
                        <div className="sidebar__section animate-in">
                            <div className="sidebar__section-title">Criteria</div>
                            <ul className="sidebar__bullet-list">
                                {config.criteria.map((c, i) => (
                                    <li key={i} className="sidebar__bullet-item">
                                        <span className="sidebar__bullet-dot" />
                                        {c}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Commentary */}
                    {config.commentary_bullets?.length > 0 && (
                        <div className="sidebar__section animate-in">
                            <div className="sidebar__section-title">Commentary Bullets</div>
                            <ul className="sidebar__bullet-list">
                                {config.commentary_bullets.map((b, i) => (
                                    <li key={i} className="sidebar__bullet-item">
                                        <span className="sidebar__bullet-dot" />
                                        {b}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Unassigned Items */}
                    {config.unassigned_items?.length > 0 && (
                        <div className="sidebar__section animate-in">
                            <div className="sidebar__section-title">Unassigned Items</div>
                            <div className="unassigned-items">
                                {config.unassigned_items.map((item, i) => (
                                    <div key={i} className="unassigned-item">{item}</div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Config Info */}
                    <div className="sidebar__section" style={{ marginTop: 'auto', opacity: 0.4 }}>
                        <div className="sidebar__section-title">Quick Help</div>
                        <ul className="sidebar__bullet-list">
                            <li className="sidebar__bullet-item" style={{ fontSize: 10 }}>
                                <span className="sidebar__bullet-dot" />
                                Ctrl+V — Toggle video
                            </li>
                            <li className="sidebar__bullet-item" style={{ fontSize: 10 }}>
                                <span className="sidebar__bullet-dot" />
                                Ctrl+B — Toggle notes
                            </li>
                            <li className="sidebar__bullet-item" style={{ fontSize: 10 }}>
                                <span className="sidebar__bullet-dot" />
                                Drop .json to load config
                            </li>
                        </ul>
                    </div>
                </div>
            </aside>
        </div>
    );
}
