/**
 * CompositeCaptureService — DEP-OVR-002
 * canvas.captureStream(30) + MediaRecorder producing 9:16 vertical video.
 * Merges canvas video track with microphone audio track.
 * Format detection: MP4 on iOS Safari, WebM VP9 on Android/Desktop.
 * Upload uses pending_background status (Phase2-M02 Background Upload Rule).
 */

export class CompositeCaptureService {
  constructor({ canvas, audioStream, onDataAvailable }) {
    this._canvas = canvas;
    this._audioStream = audioStream;
    this._onDataAvailable = onDataAvailable || (() => {});
    this._mediaRecorder = null;
    this._chunks = [];
    this._status = 'idle';
    this._startedAt = null;
    this._stoppedAt = null;
  }

  static detectMediaFormat() {
    if (typeof MediaRecorder === 'undefined') return null;
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    if (isIOS) {
      if (MediaRecorder.isTypeSupported('video/mp4;codecs=avc1')) return 'video/mp4;codecs=avc1';
      if (MediaRecorder.isTypeSupported('video/mp4')) return 'video/mp4';
    }
    if (MediaRecorder.isTypeSupported('video/webm;codecs=vp9')) return 'video/webm;codecs=vp9';
    if (MediaRecorder.isTypeSupported('video/webm')) return 'video/webm';
    return null;
  }

  start({ frameRate = 30, videoBitrate = 4000000 } = {}) {
    if (!this._canvas || typeof this._canvas.captureStream !== 'function') {
      this._status = 'failed_recoverable';
      return false;
    }

    const canvasStream = this._canvas.captureStream(frameRate);
    const combinedStream = new MediaStream();

    // Add canvas video track
    for (const track of canvasStream.getVideoTracks()) {
      combinedStream.addTrack(track);
    }

    // Add microphone audio track
    if (this._audioStream) {
      for (const track of this._audioStream.getAudioTracks()) {
        combinedStream.addTrack(track);
      }
    }

    const mimeType = CompositeCaptureService.detectMediaFormat();
    if (!mimeType) {
      this._status = 'failed_recoverable';
      return false;
    }

    const options = { mimeType, videoBitsPerSecond: videoBitrate };
    this._mediaRecorder = new MediaRecorder(combinedStream, options);
    this._chunks = [];

    this._mediaRecorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        this._chunks.push(e.data);
        this._onDataAvailable(e.data);
      }
    };

    this._mediaRecorder.onstop = () => {
      this._stoppedAt = Date.now();
      this._status = 'stopped';
    };

    this._mediaRecorder.onerror = () => {
      this._status = 'failed_recoverable';
    };

    this._mediaRecorder.start(1000); // 1-second timeslice
    this._startedAt = Date.now();
    this._status = 'recording';
    return true;
  }

  stop() {
    if (this._mediaRecorder && this._mediaRecorder.state !== 'inactive') {
      this._mediaRecorder.stop();
    }
  }

  pause() {
    if (this._mediaRecorder && this._mediaRecorder.state === 'recording') {
      this._mediaRecorder.pause();
      this._status = 'paused_backgrounded';
    }
  }

  resume() {
    if (this._mediaRecorder && this._mediaRecorder.state === 'paused') {
      this._mediaRecorder.resume();
      this._status = 'recording';
    }
  }

  getBlob() {
    if (this._chunks.length === 0) return null;
    const mimeType = CompositeCaptureService.detectMediaFormat() || 'video/webm';
    return new Blob(this._chunks, { type: mimeType });
  }

  getMetadata() {
    const blob = this.getBlob();
    return {
      status: this._status,
      startedAt: this._startedAt,
      stoppedAt: this._stoppedAt,
      durationMs: this._stoppedAt && this._startedAt ? this._stoppedAt - this._startedAt : 0,
      blobSizeBytes: blob ? blob.size : 0,
      uploadStatus: 'pending_background',
      audioTrackPresent: !!(this._audioStream && this._audioStream.getAudioTracks().length > 0),
      videoTrackPresent: true,
    };
  }

  getStatus() {
    return this._status;
  }
}
