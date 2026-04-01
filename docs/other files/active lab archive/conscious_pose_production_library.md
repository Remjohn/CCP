# ConsciousPose Production Library — Full Catalog

> **Version:** 2.0 · **Date:** 2026-03-29
> **ID Schema:** `CP-{LAYER}-{NUMBER}` (ControlNet production reference)
> **Total:** 36 Body + 36 Hands + 24 Gaze + 24 Scene + 24 Mood Visual + 24 Props = **168 composable atoms**

---

## Catalog 1: BODY POSITIONS (36)

### Standing — Authority & Coaching (12)

| ID | Position | Signal | Mood Fit | Archetype Fit |
| :--- | :--- | :--- | :--- | :--- |
| CP-B-001 | `standing_square_shoulders_back` | Full authority, grounded | Status / Processing | The Educator, The Challenger |
| CP-B-002 | `standing_lean_forward_15deg` | Engagement, "I care about this" | Processing / Discovery | The Storyteller, The Mentor |
| CP-B-003 | `standing_lean_back_casual` | Relaxed authority, "No pressure" | Escape-Cooling / Status | The Philosopher, The Observer |
| CP-B-004 | `standing_power_wide_stance` | Dominance, confidence | Status-Upward | The Challenger, The Warrior |
| CP-B-005 | `standing_contrapposto_weight_shift` | Elegance, relaxed confidence | Escape-Maintenance / Status | The Creator, The Mentor |
| CP-B-006 | `standing_arms_behind_back` | Military authority, patience | Processing-Worldview | The Sage, The Architect |
| CP-B-007 | `standing_quarter_turn_left` | 3/4 profile, editorial elegance | Discovery / Status | The Creator, The Visionary |
| CP-B-008 | `standing_quarter_turn_right` | 3/4 profile, mirror variant | Discovery / Status | The Creator, The Visionary |
| CP-B-009 | `standing_slight_sway_hip` | Casual approachability | Escape-Cooling | The Guide, The Healer |
| CP-B-010 | `standing_at_podium` | Public speaking, teacherly | Processing / Discovery | The Educator, The Leader |
| CP-B-011 | `standing_doorway_lean` | Casual entry, "between worlds" | Escape / Discovery | The Rebel, The Guide |
| CP-B-012 | `standing_back_to_wall` | Protected confidence | Processing / Status | The Observer, The Strategist |

### Seated — Intimacy & Depth (10)

| ID | Position | Signal | Mood Fit |
| :--- | :--- | :--- | :--- |
| CP-B-013 | `seated_upright_formal` | Professional, structured | Processing / Status |
| CP-B-014 | `seated_forward_lean_elbows_knees` | Intense engagement, "let me tell you" | Processing-Deep |
| CP-B-015 | `seated_lean_back_crossed_leg` | Relaxed authority, power | Status / Escape-Maintenance |
| CP-B-016 | `seated_on_edge_of_chair` | Urgency, about to act | Discovery / Status-Upward |
| CP-B-017 | `seated_floor_cross_legged` | Vulnerability, accessibility | Processing-Deep / Escape-Cooling |
| CP-B-018 | `seated_floor_knees_up` | Casual intimacy, storytelling | Escape-Cooling |
| CP-B-019 | `seated_swivel_chair_turned` | Casual authority, "let's chat" | Escape / Discovery |
| CP-B-020 | `seated_desk_writing` | Working, creation, proof | Processing / Status |
| CP-B-021 | `seated_couch_relaxed` | Home environment, trust | Escape-Cooling |
| CP-B-022 | `seated_stool_elevated` | Interview-style, elevated | Discovery / Status |

### Dynamic & Transitional (8)

| ID | Position | Signal | Mood Fit |
| :--- | :--- | :--- | :--- |
| CP-B-023 | `walking_toward_camera` | Approach, intention | Discovery / Status |
| CP-B-024 | `walking_away_looking_back` | Invitation to follow, mystery | Discovery / Escape |
| CP-B-025 | `mid_rise_from_chair` | Action moment, decision | Discovery-Revelation |
| CP-B-026 | `reaching_forward` | Connection, giving | Processing-Deep / Escape-Cooling |
| CP-B-027 | `turning_to_face_camera` | Attention capture, pattern interrupt | All (Memetic: Timing) |
| CP-B-028 | `leaning_on_table_one_arm` | Casual authority, ownership | Status / Discovery |
| CP-B-029 | `stepping_up_elevated_surface` | Ascent, progress metaphor | Status-Upward / Discovery |
| CP-B-030 | `crouching_to_camera_level` | Meeting at their level | Processing-Deep / Escape |

### Humorous & Memetic Engine (6)

| ID | Position | Signal | BVT Function |
| :--- | :--- | :--- | :--- |
| CP-B-031 | `exaggerated_shrug_full_body` | "I don't know!" — benign violation | Benignness signal (body) |
| CP-B-032 | `dramatic_frozen_mid_action` | Pattern interrupt, absurdist freeze | Violation detection (visual) |
| CP-B-033 | `mock_running_away` | Comedic escape, self-deprecating | Psychological distance (social) |
| CP-B-034 | `victorious_arms_raised_overhead` | Celebration, peak joy | Resolution reward (dopaminergic) |
| CP-B-035 | `face_palm_body` | Self-aware failure, "we all do this" | Benign violation (self-directed) |
| CP-B-036 | `exaggerated_thinking_pose` | Comedic contemplation | Incongruity setup |

---

## Catalog 2: HAND/FINGER GESTURES (36)

### Authority & Command (8)

| ID | Gesture | Signal | Mirror Neuron Target |
| :--- | :--- | :--- | :--- |
| CP-H-001 | `index_point_camera_firm` | "This means YOU" — direct command | Gaze cueing → parasocial lock |
| CP-H-002 | `index_point_camera_relaxed_palm_up` | "Consider this" — invitation | Softened attention, trust |
| CP-H-003 | `index_point_upward` | "Key insight" — authority flag | Vertical attention → importance |
| CP-H-004 | `index_point_downward_at_surface` | "Look at the evidence" | Grounding, proof |
| CP-H-005 | `open_hand_point_elegant` | Refined direction, non-aggressive | Social sophistication |
| CP-H-006 | `palm_stop_forward` | "Pause and process" | Cognitive arrest → alpha desync |
| CP-H-007 | `finger_wag_gentle` | Playful correction, teasing | BVT benignness (warmth signal) |
| CP-H-008 | `two_finger_point_emphasis` | Double emphasis, certainty | Reinforced conviction |

### Vulnerability & Connection (8)

| ID | Gesture | Signal | Mirror Neuron Target |
| :--- | :--- | :--- | :--- |
| CP-H-009 | `palm_on_chest_heart` | "I mean this sincerely" | Corrugator inhibition → trust |
| CP-H-010 | `both_palms_up_open` | "I'm transparent, I have nothing to hide" | Full openness → safety |
| CP-H-011 | `hand_reach_toward_camera` | "Let me help" — extending | Connection seeking |
| CP-H-012 | `hands_clasped_prayer_style` | Gratitude, pleading, sincerity | Vulnerability signal |
| CP-H-013 | `hand_on_shoulder_of_other` | Comfort, mentoring | Social bonding → oxytocin |
| CP-H-014 | `gentle_touch_own_face` | Thoughtful vulnerability | DMN activation → intimacy |
| CP-H-015 | `cradling_object_gently` | Care, protection | Nurture signal |
| CP-H-016 | `hand_over_mouth_surprise` | Genuine reaction, discovery | Emotional authenticity |

### Intellectual & Structure (8)

| ID | Gesture | Signal | Mirror Neuron Target |
| :--- | :--- | :--- | :--- |
| CP-H-017 | `steepled_fingers_classic` | "I'm the authority" | Dominance → respect |
| CP-H-018 | `counting_fingers_sequential` | "Step 1, 2, 3..." — structure | ISC coherence → tracking |
| CP-H-019 | `finger_to_temple_thinking` | "Process this deeply" | Analytical → alpha desync |
| CP-H-020 | `cupped_chin_contemplation` | Deep thought, weighing options | DMN activation → projection |
| CP-H-021 | `pen_in_hand_gesturing` | Teaching authority + proof | Credibility proximity |
| CP-H-022 | `hand_framing_invisible_object` | Sizing a concept, defining | Abstract → concrete mapping |
| CP-H-023 | `pinch_precision_gesture` | "This specific detail" | Precision attention |
| CP-H-024 | `hand_chopping_emphasis` | Decisive, cutting through noise | Assertive structure |

### Energy & Celebration (6)

| ID | Gesture | Signal | Mirror Neuron Target |
| :--- | :--- | :--- | :--- |
| CP-H-025 | `thumbs_up_single` | "You've got this" — approval | Zygomaticus contagion → warmth |
| CP-H-026 | `thumbs_up_double` | "We both win" — solidarity | Shared victory |
| CP-H-027 | `fist_raised_single` | Determination, power | Peak arousal → cathartic |
| CP-H-028 | `fist_pump_victory` | Celebration, achievement | Dopaminergic reward (viewer) |
| CP-H-029 | `clapping_single_clap` | Punctuation, "let's go" | Rhythmic entrainment |
| CP-H-030 | `air_high_five_toward_camera` | Parasocial bond, "you did it" | Direct engagement |

### Neutral & Resting (6)

| ID | Gesture | Signal | Mirror Neuron Target |
| :--- | :--- | :--- | :--- |
| CP-H-031 | `relaxed_at_sides` | Calm, neutral baseline | Parasympathetic baseline |
| CP-H-032 | `hands_in_pockets_casual` | Ultra-casual, "no agenda" | Social distance reduction |
| CP-H-033 | `arms_crossed_relaxed` | Listening, reserved | Protective but open |
| CP-H-034 | `one_hand_on_hip_casual` | Casual authority, waiting | Relaxed dominance |
| CP-H-035 | `hands_behind_head_leaning` | Total relaxation, confidence | Maximum comfort signal |
| CP-H-036 | `fidgeting_with_ring_or_bracelet` | Human imperfection, nerves | Authenticity → parasocial |

---

## Catalog 3: GAZE COMPOSITIONS (24)

### Direct Camera — Parasocial Bond (8)

| ID | Direction + Posture | Intent | CVE Gaze Vector |
| :--- | :--- | :--- | :--- |
| CP-G-001 | `direct_eyes_level_chin_level` | Equal connection, honest | MNS activation — bonding |
| CP-G-002 | `direct_eyes_level_chin_down_5deg` | Subtle authority, "I know" | Dominance → sympathetic arousal |
| CP-G-003 | `direct_eyes_level_chin_down_15deg` | Strong challenge, confrontation | High dominance → alert |
| CP-G-004 | `direct_eyes_level_chin_up_10deg` | Confidence, celebration | Aspiration → viewer elevation |
| CP-G-005 | `direct_squinted_knowing` | "We both know" — insider signal | Tribal recognition |
| CP-G-006 | `direct_wide_eyes_surprise` | Discovery, revelation | Arousal spike → attention |
| CP-G-007 | `direct_soft_smile_warm` | Warmth, BVT benignness | Safety signal → cortisol ↓ |
| CP-G-008 | `direct_through_glasses_lowered` | Editorial authority, judgment | Status → distance |

### Off-Camera — Depth & Contemplation (8)

| ID | Direction + Posture | Intent | CVE Gaze Vector |
| :--- | :--- | :--- | :--- |
| CP-G-009 | `off_left_low_contemplative` | Deep thought, memory access | DMN activation → projection |
| CP-G-010 | `off_right_low_emotional` | Emotional recall, vulnerability | Temporal lobe → affect |
| CP-G-011 | `off_left_high_aspirational` | Dreaming, future-oriented | Broadened scope → hope |
| CP-G-012 | `off_right_high_remembering` | Nostalgic, looking back | Memory retrieval |
| CP-G-013 | `upward_center_hopeful` | Aspiration, prayer-like | Spiritual openness |
| CP-G-014 | `downward_center_reflective` | Grief, heavy thought, shame | Processing → DMN |
| CP-G-015 | `distant_stare_through_camera` | "1000-yard stare" — philosophical | Deep dissociation → gravitas |
| CP-G-016 | `eyes_closed_feeling` | Inner experience, meditation | Full inward focus |

### Directed — Attention Transfer (8)

| ID | Direction + Posture | Intent | CVE Gaze Vector |
| :--- | :--- | :--- | :--- |
| CP-G-017 | `at_prop_whiteboard` | Teaching, evidence | Gaze cueing → attention transfer |
| CP-G-018 | `at_prop_laptop_screen` | Results, data, proof | Evidence proximity |
| CP-G-019 | `at_prop_book` | Citation, wisdom reference | Authority proof |
| CP-G-020 | `at_character_2_empathic` | Empathy with other person | Social bonding extension |
| CP-G-021 | `at_character_2_confronting` | Challenge, accountability | Social tension |
| CP-G-022 | `at_own_hand_gesture` | Self-reference, showing | Self-directed attention |
| CP-G-023 | `side_eye_knowing` | Humor, irony, "see what I did?" | BVT violation acknowledgment |
| CP-G-024 | `glancing_back_mid_turn` | "Follow me" — invitation | Movement cueing |

---

## Catalog 4: SCENE / CAMERA COMPOSITIONS (24)

### Framing × Angle (12)

| ID | Framing | Angle | Whitespace | Primary Use |
| :--- | :--- | :--- | :--- | :--- |
| CP-S-001 | `extreme_closeup_face_only` | Straight | 35% | Processing-Deep: vulnerability, emotional |
| CP-S-002 | `closeup_head_shoulders` | Straight | 40% | All: the workhorse emotional framing |
| CP-S-003 | `closeup_30deg_left` | 30° L | 40% | Processing/Discovery: editorial depth |
| CP-S-004 | `closeup_30deg_right` | 30° R | 40% | Processing/Discovery: editorial depth |
| CP-S-005 | `medium_shot_waist_up` | Straight | 45% | Teaching, explanation, gestures visible |
| CP-S-006 | `medium_shot_low_angle` | Low 15° | 45% | Status: making subject dominant |
| CP-S-007 | `medium_shot_high_angle` | High 15° | 45% | Escape-Cooling: vulnerability |
| CP-S-008 | `full_body_straight` | Straight | 50% | Power poses, celebration, Status |
| CP-S-009 | `full_body_low_angle` | Low 30° | 50% | Maximum authority/heroic |
| CP-S-010 | `over_desk_slightly_elevated` | Elevated | 35% | Teaching, mentoring, professional |
| CP-S-011 | `over_shoulder_looking_back` | Behind | 45% | Mystery, invitation, Discovery |
| CP-S-012 | `side_profile_silhouette` | 90° | 55% | Contemplation, artistic, editorial |

### Environmental & Context (6)

| ID | Framing | Context | Primary Use |
| :--- | :--- | :--- | :--- |
| CP-S-013 | `environmental_wide_office` | Office/studio context | Professional credibility |
| CP-S-014 | `environmental_wide_outdoor` | Nature, openness | Escape/Discovery — freedom |
| CP-S-015 | `environmental_wide_home` | Home/living room | Escape-Cooling — comfort |
| CP-S-016 | `environmental_stage_event` | Stage, conferencing | Status — public authority |
| CP-S-017 | `environmental_coffee_shop` | Casual meeting spot | Escape — approachability |
| CP-S-018 | `environmental_gym_workout` | Fitness/health context | Discovery — embodiment |

### Format-Specific (6)

| ID | Composition | Aspect Ratio | Primary Use |
| :--- | :--- | :--- | :--- |
| CP-S-019 | `split_screen_vs_comparison` | 4:5 / 1:1 | Polls, comparisons, "this vs that" |
| CP-S-020 | `carousel_slide_consistent` | 4:5 | Carousel slides — consistent positioning |
| CP-S-021 | `9grid_tile_position` | 1:1 | 9-grid mosaic positioning |
| CP-S-022 | `story_format_vertical` | 9:16 | Stories — full vertical |
| CP-S-023 | `banner_wide_cinematic` | 16:9 | Covers, headers, banners |
| CP-S-024 | `meme_template_centered` | 1:1 / 4:5 | Memetic Engine — text-safe zones |

---

## Catalog 5: MOOD VISUAL — LIGHTING & COLOR (24)

### Processing Mode (6)

| ID | Lighting | Kelvin | Saturation | Shadow | Psychological Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CP-MV-001 | `processing_warm_intimate` | 3200K | 35% | Soft diffused | Depth — safe container for hard truths |
| CP-MV-002 | `processing_dramatic_rembrandt` | 2800K | 25% | Hard chiaroscuro | Worldview construction — gravitas |
| CP-MV-003 | `processing_twilight_contemplative` | 3500K | 40% | Gradient soft | Deep insight — sacred space |
| CP-MV-004 | `processing_library_scholarly` | 3800K | 45% | Even, warm | Intellectual authority |
| CP-MV-005 | `processing_candlelight_vulnerable` | 2400K | 30% | Very soft, warm | Maximum intimacy + vulnerability |
| CP-MV-006 | `processing_morning_clarity` | 4200K | 40% | Clean, directional | Post-processing clarity, resolution |

### Escape Mode (6)

| ID | Lighting | Kelvin | Saturation | Shadow | Psychological Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CP-MV-007 | `escape_cooling_golden_hour` | 5000K | 55% | Warm, minimal | Nervous system downregulation |
| CP-MV-008 | `escape_cooling_soft_pastel` | 4500K | 45% | Flat, gentle | Anxiety reduction — safe space |
| CP-MV-009 | `escape_warming_bright_energetic` | 5500K | 70% | Dynamic, high-key | Energy injection — depleted state |
| CP-MV-010 | `escape_warming_sunset_vibrant` | 5800K | 65% | Warm dramatic | Arousal through beauty |
| CP-MV-011 | `escape_channeling_electric` | 6500K | 80% | High contrast | Channel HIGH/POS energy |
| CP-MV-012 | `escape_maintenance_cozy` | 4000K | 50% | Soft ambient | Content resting state |

### Discovery Mode (6)

| ID | Lighting | Kelvin | Saturation | Shadow | Psychological Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CP-MV-013 | `discovery_clean_editorial` | 5000K | 50% | Clean, balanced | Cognitive broadening — curiosity |
| CP-MV-014 | `discovery_lab_clinical` | 5500K | 40% | Even, cool | Scientific authority — data |
| CP-MV-015 | `discovery_spotlight_reveal` | 5200K | 55% | Spot + ambient | Revelation moment — "aha!" |
| CP-MV-016 | `discovery_blue_hour` | 6000K | 45% | Cool dramatic | Counter-intuitive — challenge |
| CP-MV-017 | `discovery_overcast_neutral` | 5800K | 35% | Flat, objective | Neutral analysis — no bias |
| CP-MV-018 | `discovery_neon_modern` | 6500K | 75% | High-key, edgy | Modern insight — tech-forward |

### Status Mode (6)

| ID | Lighting | Kelvin | Saturation | Shadow | Psychological Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CP-MV-019 | `status_polished_premium_dark` | 4000K | 45% | Controlled, premium | Aspirational authority |
| CP-MV-020 | `status_boardroom_power` | 4200K | 50% | Hard directional | Corporate dominance |
| CP-MV-021 | `status_gala_luxurious` | 3800K | 55% | Rich, warm | Premium lifestyle |
| CP-MV-022 | `status_stage_spotlight` | 5000K | 60% | Isolated spot | Public recognition |
| CP-MV-023 | `status_minimal_contrast` | 4500K | 35% | High B&W contrast | Editorial luxury — magazine |
| CP-MV-024 | `status_victorious_golden` | 4800K | 65% | Warm spotlight | Peak achievement — celebration |

---

## Catalog 6: PROPS & INTERACTION OBJECTS (24)

### Professional (6)

| ID | Prop | Interaction | Scene Constraint |
| :--- | :--- | :--- | :--- |
| CP-P-001 | `whiteboard_marker` | Writing, pointing at content | Requires CP-S-005 or wider |
| CP-P-002 | `laptop_open_screen_visible` | Reviewing data, results | Desk framing preferred |
| CP-P-003 | `tablet_showing_to_camera` | Proof, screenshot, evidence | Medium shot |
| CP-P-004 | `book_open_reading` | Wisdom, citation | Seated or standing |
| CP-P-005 | `notebook_journal_pen` | Personal reflection, writing | Intimate framing |
| CP-P-006 | `presentation_clicker` | Stage authority, advancing | Standing + stage |

### Personal & Warmth (6)

| ID | Prop | Interaction | Scene Constraint |
| :--- | :--- | :--- | :--- |
| CP-P-007 | `coffee_mug_holding` | Approachability, morning routine | Medium or closer |
| CP-P-008 | `phone_showing_text` | Testimonial, DM screenshot | Close-up hand |
| CP-P-009 | `glasses_removing_moment` | "Let me be real" transition | Close-up face |
| CP-P-010 | `water_bottle_active` | Health, vitality | Any |
| CP-P-011 | `plant_greenery_nearby` | Growth metaphor, life | Environmental |
| CP-P-012 | `mirror_self_reflection` | Self-work metaphor | Creative framing |

### Symbolic & Metaphorical (6)

| ID | Prop | Interaction | Trojan Horse Use |
| :--- | :--- | :--- | :--- |
| CP-P-013 | `clock_time_piece` | Urgency, time management | Counterfactual Activation (CPSC) |
| CP-P-014 | `chess_piece_strategic` | Strategy, calculated moves | Processing-Worldview |
| CP-P-015 | `trophy_award` | Achievement, validation | Status — social proof |
| CP-P-016 | `broken_chain_freedom` | Liberation, breakthrough | Discovery-Revelation |
| CP-P-017 | `map_or_compass` | Direction, finding path | Escape → Discovery transition |
| CP-P-018 | `key_or_lock` | Unlocking potential | Trojan Horse payload |

### Memetic & Humorous (6)

| ID | Prop | Interaction | BVT Function |
| :--- | :--- | :--- | :--- |
| CP-P-019 | `oversized_glasses_comedic` | Exaggerated "expert" look | Violation (logical) + benign (playful) |
| CP-P-020 | `red_flag_literal` | "Red flag" meme — holding flag | Violation (social norm) visual |
| CP-P-021 | `sticky_notes_everywhere` | Overwhelm, chaos | Self-deprecating violation |
| CP-P-022 | `microphone_drop_gesture` | "Mic drop" — definitive | Resolution reward (peak) |
| CP-P-023 | `dumpster_fire_small_prop` | "Everything's fine" irony | Absurdist violation |
| CP-P-024 | `none` | Pure body language, no prop | Default baseline |

---

## Catalog 7: MULTI-CHARACTER COMPOSITIONS (12)

| ID | Composition | Characters | Spatial Rule | Primary Use |
| :--- | :--- | :--- | :--- | :--- |
| CP-MC-001 | `solo` | 1 | Standard single | Default — 80% of content |
| CP-MC-002 | `coach_client_seated_facing` | 2 | 45° angle, eye level | Coaching session, mentoring |
| CP-MC-003 | `coach_client_standing_consoling` | 2 | Close, hand on shoulder | Emotional support |
| CP-MC-004 | `coach_client_walking_together` | 2 | Side by side, mid-stride | Journey metaphor |
| CP-MC-005 | `coach_vs_opponent_split` | 2 | Split screen, facing | Comparison, "this vs that" |
| CP-MC-006 | `coach_group_leading` | 1+3 | Coach foreground, group back | Leadership, authority |
| CP-MC-007 | `coach_group_circle` | 1+4 | Circular, equal height | Community, tribe |
| CP-MC-008 | `two_coaches_handshake` | 2 | Facing, clasped hands | Partnership, collaboration |
| CP-MC-009 | `coach_presenting_to_audience` | 1+crowd | Stage perspective | Webinar, event, Status |
| CP-MC-010 | `before_after_same_person` | 1×2 | Same person, different states | Transformation story |
| CP-MC-011 | `emotional_closeup_pair` | 2 | Tight framing, faces close | Deep connection, emotional |
| CP-MC-012 | `confrontation_opposing` | 2 | Facing, tension in gap | Challenge, debate |

---

## Catalog 8: MEMETIC ENGINE VISUAL SUPPORT

The 14 humor architectures from the Memetic Engine each require specific visual compositions. These are **composition recipes** — not new atoms, but specific combinations of the atoms above:

| # | Humor Architecture | Recommended Body | Hands | Gaze | Scene | BVT Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Observational** | CP-B-003 or CP-B-005 | CP-H-005 or CP-H-034 | CP-G-005 (knowing) | CP-S-002 | Benign: familiar recognition |
| 2 | **Self-Deprecating** | CP-B-035 (facepalm) | CP-H-010 (palms up) | CP-G-001 (direct) | CP-S-002 | Benign: self as target |
| 3 | **Absurdist** | CP-B-032 (frozen) or CP-B-036 | CP-H-016 (surprise) | CP-G-006 (wide eyes) | CP-S-024 (meme) | Violation: logical/nonsense |
| 4 | **Sarcastic** | CP-B-007 (quarter turn) | CP-H-017 (steepled) | CP-G-023 (side eye) | CP-S-003 | Violation: norm via tone |
| 5 | **Understatement** | CP-B-003 (lean back) | CP-H-031 (relaxed) | CP-G-001 (direct calm) | CP-S-002 | Benign: minimization |
| 6 | **Exaggeration** | CP-B-031 (shrug) or CP-B-034 | CP-H-027 (fist raised) | CP-G-004 (chin up) | CP-S-008 (full body) | Violation: scale |
| 7 | **Callback** | CP-B-002 (lean forward) | CP-H-003 (point up) | CP-G-005 (knowing) | CP-S-002 | Resolution: recognition |
| 8 | **Ironic Contrast** | CP-B-005 (contrapposto) | CP-H-034 (hand on hip) | CP-G-023 (side eye) | CP-S-019 (split) | Incongruity: visual |
| 9 | **Thought Experiment** | CP-B-014 (seated forward) | CP-H-019 (temple) | CP-G-009 (off contemplative) | CP-S-001 (extreme CU) | Setup: hypothetical |
| 10 | **Pattern Interrupt** | CP-B-027 (turning) or CP-B-032 | CP-H-006 (stop) | CP-G-006 (wide) | CP-S-024 (meme) | Violation: expectation |
| 11 | **Metaphor Collision** | CP-B-012 (arms wide) | CP-H-022 (framing) | CP-G-001 (direct) | CP-S-005 (medium) | Incongruity: semantic |
| 12 | **Dark Humor** | CP-B-006 (arms behind back) | CP-H-009 (chest) | CP-G-002 (chin down) | CP-S-012 (side profile) | Violation: moral |
| 13 | **Deadpan** | CP-B-001 (square) | CP-H-031 (relaxed) | CP-G-001 (direct flat) | CP-S-002 | Benign: emotional distance |
| 14 | **Running Gag** | Variable (recognizable) | Variable (recognizable) | CP-G-005 (knowing) | Consistent per series | Resolution: pattern |

---

## Catalog 9: ARCHETYPE × MOOD COMPOSITION RECIPES

Each content archetype has a default visual composition recipe. Abel overrides when the Psychological Routing Brief demands it.

| Archetype Family | Default Body | Default Hands | Default Gaze | Default Scene | Default Mood Visual |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **The Educator** | CP-B-010 / CP-B-005 | CP-H-018 / CP-H-003 | CP-G-001 | CP-S-005 | CP-MV-004 / CP-MV-013 |
| **The Challenger** | CP-B-004 / CP-B-001 | CP-H-001 / CP-H-024 | CP-G-003 | CP-S-006 | CP-MV-002 / CP-MV-020 |
| **The Storyteller** | CP-B-014 / CP-B-017 | CP-H-022 / CP-H-009 | CP-G-009 / CP-G-001 | CP-S-001 / CP-S-002 | CP-MV-001 / CP-MV-003 |
| **The Mentor** | CP-B-002 / CP-B-013 | CP-H-011 / CP-H-009 | CP-G-001 / CP-G-007 | CP-S-002 / CP-S-010 | CP-MV-001 / CP-MV-007 |
| **The Rebel** | CP-B-011 / CP-B-028 | CP-H-034 / CP-H-027 | CP-G-002 / CP-G-023 | CP-S-006 / CP-S-011 | CP-MV-016 / CP-MV-019 |
| **The Healer** | CP-B-017 / CP-B-026 | CP-H-010 / CP-H-013 | CP-G-007 / CP-G-010 | CP-S-001 / CP-S-015 | CP-MV-005 / CP-MV-008 |
| **The Strategist** | CP-B-006 / CP-B-020 | CP-H-017 / CP-H-020 | CP-G-001 / CP-G-002 | CP-S-010 / CP-S-013 | CP-MV-004 / CP-MV-020 |

---

## ControlNet Asset ID Schema

Every rendered ControlNet conditioning file follows this naming convention:

```
{CP_COMPOSITION_ID}_{VARIANT}_{RENDER_TYPE}.png
```

**Example:**
```
CP-B-014_CP-H-017_CP-G-001_CP-S-002_CP-MV-001_v01_depth.png
CP-B-014_CP-H-017_CP-G-001_CP-S-002_CP-MV-001_v01_openpose.png
CP-B-014_CP-H-017_CP-G-001_CP-S-002_CP-MV-001_v01_preview.png
```

**Render types per asset:**
- `_depth.png` — Depth map for ControlNet Depth
- `_openpose.png` — OpenPose skeleton for ControlNet Pose
- `_normal.png` — Normal map (optional, for advanced lighting control)
- `_preview.png` — Full render preview for operator reference
- `.json` — Complete composition specification (all 8 layers)

**Asset storage:**
```
controlnet_library/
├── body/           ← 36 base body position renders
├── compositions/   ← Pre-composed presets (curated combos)
│   ├── processing/
│   ├── escape/
│   ├── discovery/
│   ├── status/
│   └── memetic/
├── multi_character/
└── manifest.json   ← Master index of all assets
```
