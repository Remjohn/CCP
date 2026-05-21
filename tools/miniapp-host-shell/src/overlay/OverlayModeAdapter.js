/**
 * OverlayModeAdapter — DEP-OVR-006
 * Interface that each reaction mode implements to register its visual layout.
 * Each mode provides mount/unmount lifecycle, round state transitions, and element registration.
 */

export class OverlayModeAdapter {
  /**
   * @param {Object} config - OverlayModeConfig from backend
   * @param {Object} overlayContainer - PixiJS Container from OverlayRenderer
   * @param {Object} palette - ResolvedPalette from DPA Engine
   */
  constructor({ config, overlayContainer, palette }) {
    this._config = config;
    this._container = overlayContainer;
    this._palette = palette;
    this._mounted = false;
  }

  /**
   * Mount mode-specific overlay elements onto the container.
   * Must be implemented by each reaction mode.
   */
  async mountLayout() {
    throw new Error('OverlayModeAdapter.mountLayout() must be implemented by the mode.');
  }

  /**
   * Handle a round state transition.
   * @param {Object} stateChange - { fromState, toState, roundIndex, payload }
   */
  onRoundStateChange(stateChange) {
    throw new Error('OverlayModeAdapter.onRoundStateChange() must be implemented by the mode.');
  }

  /**
   * Return the current visible element state for the interaction journal.
   * @returns {Object} Mode-specific element snapshot
   */
  getElementSnapshot() {
    throw new Error('OverlayModeAdapter.getElementSnapshot() must be implemented by the mode.');
  }

  /**
   * Unmount and clean up mode-specific overlay elements.
   */
  unmountLayout() {
    if (this._container) {
      this._container.removeChildren();
    }
    this._mounted = false;
  }

  isMounted() {
    return this._mounted;
  }

  getConfig() {
    return this._config;
  }
}
