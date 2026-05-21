/**
 * AdaptiveResolutionManager — DEP-OVR-007
 * Detects device capability and selects 720p or 1080p canvas resolution.
 * Falls back to 540×960 at 24fps on low-end devices.
 * Logs resolution_downgraded=true when downgrade occurs.
 */

const RESOLUTION_PROFILES = {
  high: { width: 1080, height: 1920, frameRate: 30, videoBitrate: 6000000, tier: 'high' },
  mid: { width: 720, height: 1280, frameRate: 30, videoBitrate: 4000000, tier: 'mid' },
  low: { width: 540, height: 960, frameRate: 24, videoBitrate: 2000000, tier: 'low' },
};

export class AdaptiveResolutionManager {
  constructor() {
    this._currentProfile = null;
    this._downgraded = false;
  }

  detect() {
    const deviceMemory = navigator.deviceMemory || 4;
    const hardwareConcurrency = navigator.hardwareConcurrency || 4;
    const screenWidth = window.screen.width || 720;

    let tier = 'mid';
    if (deviceMemory >= 6 && hardwareConcurrency >= 6 && screenWidth >= 1080) {
      tier = 'high';
    } else if (deviceMemory <= 2 || hardwareConcurrency <= 2 || screenWidth < 720) {
      tier = 'low';
      this._downgraded = true;
    }

    this._currentProfile = { ...RESOLUTION_PROFILES[tier], resolutionDowngraded: this._downgraded };
    return this._currentProfile;
  }

  downgrade() {
    const currentTier = this._currentProfile?.tier || 'mid';
    if (currentTier === 'high') {
      this._currentProfile = { ...RESOLUTION_PROFILES.mid, resolutionDowngraded: true };
    } else if (currentTier === 'mid') {
      this._currentProfile = { ...RESOLUTION_PROFILES.low, resolutionDowngraded: true };
    }
    this._downgraded = true;
    return this._currentProfile;
  }

  getCurrentProfile() {
    return this._currentProfile || this.detect();
  }

  isDowngraded() {
    return this._downgraded;
  }
}
