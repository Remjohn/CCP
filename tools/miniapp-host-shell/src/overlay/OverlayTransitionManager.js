/**
 * OverlayTransitionManager — DEP-OVR-004
 * Animated transitions between rounds/questions/reveals via PixiJS tweens.
 * Synchronized with OverlaySoundEngine for same-frame audio cues.
 * Supports: fade, slide, scale, and color-pulse transitions.
 */

export class OverlayTransitionManager {
  constructor({ soundEngine, interactionJournal }) {
    this._soundEngine = soundEngine;
    this._journal = interactionJournal;
    this._activeTransitions = [];
  }

  async playTransition({ type, target, duration = 300, soundCue = null, fromState = null, toState = null, roundIndex = null }) {
    return new Promise((resolve) => {
      const startTime = performance.now();

      // Fire sound cue within the same frame as transition start (EXP-FBK-004)
      if (soundCue && this._soundEngine) {
        this._soundEngine.play(soundCue);
      }

      // Log transition event to interaction journal
      if (this._journal) {
        this._journal.emit({
          eventType: 'transition_played',
          fromState,
          toState,
          roundIndex,
          overlayElements: { transitionType: type, duration },
        });
      }

      const transitionId = Date.now();
      this._activeTransitions.push(transitionId);

      // Execute transition animation
      const animate = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = this._easeOutCubic(progress);

        if (target) {
          switch (type) {
            case 'fade_in':
              target.alpha = eased;
              break;
            case 'fade_out':
              target.alpha = 1 - eased;
              break;
            case 'slide_left':
              target.x = target._startX !== undefined ? target._startX * (1 - eased) : -target.width * (1 - eased);
              break;
            case 'slide_right':
              target.x = target._startX !== undefined ? target._startX + (target.width * eased) : target.width * eased;
              break;
            case 'scale_up':
              target.scale.set(eased);
              break;
            case 'scale_down':
              target.scale.set(1 - eased * 0.5);
              break;
            case 'color_pulse':
              target.alpha = 0.5 + 0.5 * Math.sin(progress * Math.PI * 2);
              break;
            default:
              break;
          }
        }

        if (progress < 1) {
          requestAnimationFrame(animate);
        } else {
          this._activeTransitions = this._activeTransitions.filter((id) => id !== transitionId);
          resolve();
        }
      };

      requestAnimationFrame(animate);
    });
  }

  _easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  hasActiveTransitions() {
    return this._activeTransitions.length > 0;
  }

  cancelAll() {
    this._activeTransitions = [];
  }
}
