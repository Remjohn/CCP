/**
 * OverlaySoundEngine — DEP-OVR-003
 * Howler.js integration for low-latency transition/timer/feedback audio sprites.
 * Sound cues fire within the same animation frame as overlay transitions (EXP-FBK-004).
 * Timer sounds follow Hypnosedation Reframing — focused drill, not panic alarm (EXP-FRC-006).
 */

export class OverlaySoundEngine {
  constructor({ soundPack = 'default' } = {}) {
    this._soundPack = soundPack;
    this._howl = null;
    this._enabled = false;
    this._initialized = false;
  }

  async initialize() {
    try {
      const { Howl } = await import('howler');

      const spritePath = `/audio/${this._soundPack}.mp3`;
      const spriteMap = this._getSpriteMap(this._soundPack);

      this._howl = new Howl({
        src: [spritePath],
        sprite: spriteMap,
        preload: true,
        html5: false,
        onload: () => { this._enabled = true; },
        onloaderror: () => { this._enabled = false; },
      });

      this._initialized = true;
    } catch {
      this._enabled = false;
      this._initialized = false;
    }
  }

  _getSpriteMap(pack) {
    const sprites = {
      default: {
        'tick_neutral': [0, 400],
        'transition_swoosh': [500, 600],
        'success_sting': [1200, 800],
        'fail_sting': [2100, 600],
        'round_start': [2800, 500],
        'round_end': [3400, 500],
        'timer_pulse': [4000, 300],
        'reveal_fanfare': [4400, 1000],
        'snap_confirm': [5500, 300],
      },
    };
    return sprites[pack] || sprites.default;
  }

  play(cueId) {
    if (!this._enabled || !this._howl) return false;
    this._howl.play(cueId);
    return true;
  }

  stop(cueId) {
    if (!this._howl) return;
    this._howl.stop(cueId);
  }

  stopAll() {
    if (!this._howl) return;
    this._howl.stop();
  }

  isEnabled() {
    return this._enabled;
  }

  isInitialized() {
    return this._initialized;
  }

  destroy() {
    if (this._howl) {
      this._howl.unload();
      this._howl = null;
    }
    this._enabled = false;
    this._initialized = false;
  }
}
