/**
 * OverlayRenderer — DEP-OVR-001
 * PixiJS v8 engine compositing camera feed + mode-specific game overlay.
 * Camera feed fills canvas background at 9:16 via VideoSource texture.
 * Overlay elements render on top via the PixiJS WebGL stage.
 * Does NOT call getUserMedia directly — receives granted stream from shell (Phase1-M03).
 */

export class OverlayRenderer {
  constructor({ canvasElement, stream, modeConfig, resolvedPalette }) {
    this._canvas = canvasElement;
    this._stream = stream;
    this._modeConfig = modeConfig;
    this._palette = resolvedPalette;
    this._app = null;
    this._cameraSprite = null;
    this._overlayContainer = null;
    this._mounted = false;
  }

  async mount() {
    const { Application, Sprite, Container, Assets } = await import('pixi.js');

    this._app = new Application();
    await this._app.init({
      canvas: this._canvas,
      width: this._modeConfig.width || 720,
      height: this._modeConfig.height || 1280,
      backgroundAlpha: 1,
      backgroundColor: this._palette?.backgroundColor || 0x1a1a2e,
    });

    // Camera background texture from granted stream
    if (this._stream && this._stream.getVideoTracks().length > 0) {
      const videoEl = document.createElement('video');
      videoEl.srcObject = this._stream;
      videoEl.playsInline = true;
      videoEl.muted = true;
      await videoEl.play();

      const { VideoSource, Texture } = await import('pixi.js');
      const videoSource = new VideoSource({ resource: videoEl, autoPlay: true });
      const texture = new Texture({ source: videoSource });
      this._cameraSprite = new Sprite(texture);
      this._cameraSprite.width = this._app.screen.width;
      this._cameraSprite.height = this._app.screen.height;
      this._app.stage.addChild(this._cameraSprite);
    } else {
      // Fallback: DPA-themed gradient background (no camera)
      const { Graphics } = await import('pixi.js');
      const bg = new Graphics();
      bg.beginFill(this._palette?.backgroundColor || 0x1a1a2e);
      bg.drawRect(0, 0, this._app.screen.width, this._app.screen.height);
      bg.endFill();
      this._app.stage.addChild(bg);
    }

    // Overlay container for mode-specific elements
    const { Container: C } = await import('pixi.js');
    this._overlayContainer = new C();
    this._app.stage.addChild(this._overlayContainer);

    this._mounted = true;
    return this._overlayContainer;
  }

  getCanvas() {
    return this._canvas;
  }

  getApp() {
    return this._app;
  }

  getOverlayContainer() {
    return this._overlayContainer;
  }

  isMounted() {
    return this._mounted;
  }

  destroy() {
    if (this._app) {
      this._app.destroy(true);
      this._app = null;
    }
    this._mounted = false;
  }
}
