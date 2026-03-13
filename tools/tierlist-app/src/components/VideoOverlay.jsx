import React, { useRef, useState, useEffect, useCallback } from 'react';

/**
 * VideoOverlay — centered video player (25-30% viewport)
 * Plays the reaction clip the coach wants to react to.
 */
export default function VideoOverlay({ videoSrc, visible, onToggle }) {
    const videoRef = useRef(null);
    const progressRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);

    useEffect(() => {
        if (!visible && videoRef.current) {
            videoRef.current.pause();
            setIsPlaying(false);
        }
    }, [visible]);

    const togglePlay = useCallback(() => {
        const video = videoRef.current;
        if (!video) return;
        if (video.paused) {
            video.play();
            setIsPlaying(true);
        } else {
            video.pause();
            setIsPlaying(false);
        }
    }, []);

    const handleTimeUpdate = useCallback(() => {
        const video = videoRef.current;
        if (!video) return;
        setCurrentTime(video.currentTime);
    }, []);

    const handleLoadedMetadata = useCallback(() => {
        const video = videoRef.current;
        if (!video) return;
        setDuration(video.duration);
    }, []);

    const handleProgressClick = useCallback((e) => {
        const video = videoRef.current;
        const bar = progressRef.current;
        if (!video || !bar) return;
        const rect = bar.getBoundingClientRect();
        const ratio = (e.clientX - rect.left) / rect.width;
        video.currentTime = ratio * video.duration;
    }, []);

    const handleEnded = useCallback(() => {
        setIsPlaying(false);
    }, []);

    function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60);
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    const progress = duration > 0 ? (currentTime / duration) * 100 : 0;
    const hasVideo = videoSrc && videoSrc.length > 0;

    return (
        <div className={`video-overlay ${!visible ? 'video-overlay--hidden' : ''}`}>
            {/* Header */}
            <div className="video-overlay__header">
                <span className="video-overlay__header-title">Reaction Clip</span>
                <button
                    className="video-overlay__close"
                    onClick={onToggle}
                    title="Hide video (Ctrl+V)"
                >
                    ✕
                </button>
            </div>

            {/* Video Content */}
            <div className="video-overlay__content">
                {hasVideo ? (
                    <video
                        ref={videoRef}
                        className="video-overlay__video"
                        src={videoSrc}
                        onTimeUpdate={handleTimeUpdate}
                        onLoadedMetadata={handleLoadedMetadata}
                        onEnded={handleEnded}
                        preload="metadata"
                    />
                ) : (
                    <div className="video-overlay__placeholder">
                        <div className="video-overlay__placeholder-icon">🎬</div>
                        <div>No video loaded</div>
                        <div style={{ fontSize: 11, color: '#6b6b85' }}>
                            Add a video path to your config JSON
                        </div>
                    </div>
                )}
            </div>

            {/* Controls */}
            <div className="video-overlay__controls">
                <button
                    className="video-overlay__play-btn"
                    onClick={togglePlay}
                    disabled={!hasVideo}
                    title={isPlaying ? 'Pause (Space)' : 'Play (Space)'}
                >
                    {isPlaying ? '⏸' : '▶'}
                </button>
                <span className="video-overlay__time">{formatTime(currentTime)}</span>
                <div
                    className="video-overlay__progress"
                    ref={progressRef}
                    onClick={handleProgressClick}
                >
                    <div
                        className="video-overlay__progress-bar"
                        style={{ width: `${progress}%` }}
                    />
                </div>
                <span className="video-overlay__time">{formatTime(duration)}</span>
            </div>
        </div>
    );
}
