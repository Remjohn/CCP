# AR Overlay Audio Sprite Packs

This directory contains audio sprite packs for the AR Overlay Capture Pipeline.

## Format
Each mode pack is a single MP3 file with named sprite regions:
- `tick_neutral` — neutral timer tick (EXP-FRC-006: focused, not panicked)
- `transition_swoosh` — round/state transition
- `success_sting` — correct answer / pass feedback
- `fail_sting` — incorrect / fail feedback
- `round_start` — round begin cue
- `round_end` — round complete cue
- `timer_pulse` — periodic timer pulse
- `reveal_fanfare` — score/result reveal
- `snap_confirm` — element placement confirmation

## Packs
- `default.mp3` — universal pack for all modes
- Mode-specific packs override the default when specified in `OverlayModeConfig.sound_pack`
