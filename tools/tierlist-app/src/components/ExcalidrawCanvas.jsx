import React, { useRef, useState, useEffect, useCallback } from 'react';

/**
 * ExcalidrawCanvas — wraps @excalidraw/excalidraw
 * Generates and renders tier list / rating elements from config data.
 */
export default function ExcalidrawCanvas({ config, excalidrawAPI, setExcalidrawAPI }) {
    const [ExcalidrawComp, setExcalidrawComp] = useState(null);

    // Dynamic import (Excalidraw doesn't support SSR)
    useEffect(() => {
        import('@excalidraw/excalidraw').then((mod) => {
            setExcalidrawComp(() => mod.Excalidraw);
        });
    }, []);

    const initialData = useCallback(() => {
        if (!config) return { elements: [], appState: { viewBackgroundColor: '#1a1a2e' } };
        return {
            elements: generateElements(config),
            appState: {
                viewBackgroundColor: '#1a1a2e',
                gridSize: null,
                theme: 'dark',
            },
        };
    }, [config]);

    if (!ExcalidrawComp) {
        return (
            <div style={{
                width: '100%', height: '100%',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: '#6b6b85', fontSize: 14, fontFamily: 'Inter, sans-serif'
            }}>
                Loading Excalidraw…
            </div>
        );
    }

    return (
        <div className="excalidraw-wrapper">
            <ExcalidrawComp
                initialData={initialData()}
                theme="dark"
                excalidrawAPI={(api) => setExcalidrawAPI(api)}
                UIOptions={{
                    canvasActions: {
                        saveToActiveFile: false,
                        loadScene: false,
                    },
                }}
            />
        </div>
    );
}

/* ═══════════════════════════════════════════════════════
   Element Generators
   ═══════════════════════════════════════════════════════ */

let seedCounter = 1000;
function nextSeed() { return seedCounter++; }
function uid(prefix, i) { return `${prefix}-${i}-${nextSeed()}`; }

function baseProps(overrides = {}) {
    return {
        angle: 0,
        fillStyle: 'solid',
        strokeWidth: 2,
        strokeStyle: 'solid',
        roughness: 1,
        opacity: 100,
        seed: nextSeed(),
        version: 1,
        versionNonce: nextSeed(),
        isDeleted: false,
        groupIds: [],
        boundElements: null,
        link: null,
        locked: false,
        ...overrides,
    };
}

function rect(id, x, y, w, h, bg, stroke = '#1e1e1e', extra = {}) {
    return {
        type: 'rectangle',
        id,
        x, y, width: w, height: h,
        strokeColor: stroke,
        backgroundColor: bg,
        roundness: { type: 3 },
        ...baseProps(extra),
    };
}

function text(id, x, y, content, fontSize = 20, color = '#f0f0f5', extra = {}) {
    const lineHeight = 1.25;
    const lines = content.split('\n');
    return {
        type: 'text',
        id,
        x, y,
        width: content.length * fontSize * 0.6,
        height: fontSize * lineHeight * lines.length,
        text: content,
        fontSize,
        fontFamily: 1, // Virgil (hand-drawn)
        textAlign: 'left',
        verticalAlign: 'top',
        strokeColor: color,
        backgroundColor: 'transparent',
        originalText: content,
        autoResize: true,
        lineHeight,
        containerId: null,
        ...baseProps(extra),
    };
}

/**
 * Generate Excalidraw elements from config JSON
 */
function generateElements(config) {
    const elements = [];

    if (config.mode === 'tier-list') {
        generateTierList(config, elements);
    } else {
        generateRatingScale(config, elements);
    }

    return elements;
}

/* ═══════════════════════════════════════════════════════
   TIER LIST GENERATOR
   ═══════════════════════════════════════════════════════
   Classic tier list layout matching reference screenshots:

   ┌────────────────────────────────────────────────────┐
   │  Title: "Comfort Food Ranked by Comfort"           │
   ├────┬───────────────────────────────────────────────┤
   │ S  │  [img] [img] [img]                            │
   ├────┼───────────────────────────────────────────────┤
   │ A  │  [img] [img] [img] [img]                      │
   ├────┼───────────────────────────────────────────────┤
   │ B  │  [img] [img]                                  │
   ├────┼───────────────────────────────────────────────┤
   │ C  │                                               │
   ├────┼───────────────────────────────────────────────┤
   │ D  │                                               │
   ├────┼───────────────────────────────────────────────┤
   │ E  │                                               │
   ├────┼───────────────────────────────────────────────┤
   │ F  │                                               │
   ├────┴───────────────────────────────────────────────┤
   │  🍕  🥤  🍉  🌭  🍔  🍗  🌮  🧁  🥞  🍟         │
   │               ITEM POOL (drag up)                  │
   └────────────────────────────────────────────────────┘
   ═══════════════════════════════════════════════════════ */

const TIER_CONFIG = [
    { key: 'S', color: '#FF6B6B', textColor: '#1a1a1a' },  // coral red
    { key: 'A', color: '#FF9E4A', textColor: '#1a1a1a' },  // orange
    { key: 'B', color: '#FFE066', textColor: '#1a1a1a' },  // yellow
    { key: 'C', color: '#6BCB77', textColor: '#1a1a1a' },  // green
    { key: 'D', color: '#4DABF7', textColor: '#1a1a1a' },  // blue
    { key: 'E', color: '#CC99FF', textColor: '#1a1a1a' },  // lavender
    { key: 'F', color: '#FFB3D9', textColor: '#1a1a1a' },  // pink
];

function generateTierList(config, elements) {
    const startX = 60;
    const startY = 80;
    const labelW = 70;          // compact label square
    const rowH = 80;            // row height
    const rowW = 900;           // full-width row
    const gap = 4;              // tight gap between rows
    const itemSize = 64;        // square image slots
    const itemGap = 8;

    // ─── Title ────────────────────────────────────
    elements.push(text(
        uid('title', 0),
        startX, 20,
        config.title || 'TIER LIST',
        28,
        '#e0e0e8',
        { roughness: 0 },
    ));

    // ─── Tier Rows ────────────────────────────────
    TIER_CONFIG.forEach((tier, i) => {
        const y = startY + i * (rowH + gap);
        const tierData = config.tiers?.[tier.key];

        // Label square (colored, hand-drawn)
        elements.push(rect(
            uid('tier-label-bg', i),
            startX, y, labelW, rowH,
            tier.color, tier.color,
            { roughness: 2, strokeWidth: 1 },
        ));

        // Label letter (bold, centered in square)
        elements.push(text(
            uid('tier-letter', i),
            startX + labelW / 2 - 12, y + rowH / 2 - 18,
            tier.key,
            32,
            tier.textColor,
            { textAlign: 'center', roughness: 0 },
        ));

        // Row area (dark, hand-drawn border)
        elements.push(rect(
            uid('tier-row', i),
            startX + labelW, y, rowW, rowH,
            '#2d2d3d', '#3d3d4d',
            { roughness: 1, strokeWidth: 1 },
        ));

        // Pre-placed items in this tier (square image slots)
        if (tierData?.items) {
            tierData.items.forEach((item, j) => {
                const itemX = startX + labelW + itemGap + j * (itemSize + itemGap);
                const itemY = y + (rowH - itemSize) / 2;

                // Item image slot (slightly rough, dark fill)
                elements.push(rect(
                    uid('item-slot', i * 100 + j),
                    itemX, itemY, itemSize, itemSize,
                    '#3a3a4a', '#505068',
                    { roughness: 1, strokeWidth: 1 },
                ));

                // Item label (small, below center)
                const label = typeof item === 'string' ? item : item.name || '';
                if (label) {
                    elements.push(text(
                        uid('item-label', i * 100 + j),
                        itemX + 4, itemY + itemSize / 2 - 8,
                        label.length > 10 ? label.substring(0, 9) + '…' : label,
                        11,
                        '#c0c0d0',
                        { roughness: 0 },
                    ));
                }
            });
        }
    });

    // ─── Item Pool (bottom) ───────────────────────
    const poolY = startY + TIER_CONFIG.length * (rowH + gap) + 20;
    const poolItems = config.unassigned_items || [];

    if (poolItems.length > 0) {
        // Pool background
        elements.push(rect(
            uid('pool-bg', 0),
            startX, poolY, labelW + rowW, itemSize + 24,
            '#252535', '#3d3d4d',
            { roughness: 1, strokeWidth: 1, strokeStyle: 'dashed' },
        ));

        // Pool label
        elements.push(text(
            uid('pool-label', 0),
            startX + labelW + rowW / 2 - 80, poolY + itemSize + 6,
            'ITEM POOL — drag items up',
            11,
            '#6b6b85',
            { roughness: 0 },
        ));

        // Pool item slots (square image thumbnails)
        poolItems.forEach((item, i) => {
            const ix = startX + itemGap + i * (itemSize + itemGap);
            const iy = poolY + 10;

            // Square slot
            elements.push(rect(
                uid('pool-slot', i),
                ix, iy, itemSize, itemSize,
                '#3a3a4a', '#505068',
                { roughness: 1, strokeWidth: 1 },
            ));

            // Item label inside
            const label = typeof item === 'string' ? item : item.name || '';
            if (label) {
                elements.push(text(
                    uid('pool-label-item', i),
                    ix + 4, iy + itemSize / 2 - 8,
                    label.length > 10 ? label.substring(0, 9) + '…' : label,
                    11,
                    '#c0c0d0',
                    { roughness: 0 },
                ));
            }
        });
    }

    // ─── Criteria (subtle, top-right corner) ──────
    if (config.criteria?.length) {
        const crX = startX + labelW + rowW + 30;
        elements.push(text(
            uid('criteria-header', 0),
            crX, startY,
            'CRITERIA',
            14,
            '#6b6b85',
            { roughness: 0 },
        ));
        config.criteria.forEach((c, i) => {
            elements.push(text(
                uid('criteria', i),
                crX, startY + 24 + i * 22,
                `• ${c}`,
                12,
                '#505068',
                { roughness: 0 },
            ));
        });
    }

    // ─── Commentary (below criteria) ──────────────
    if (config.commentary_bullets?.length) {
        const crX = startX + labelW + rowW + 30;
        const cbY = startY + 24 + (config.criteria?.length || 0) * 22 + 20;
        elements.push(text(
            uid('commentary-header', 0),
            crX, cbY,
            'NOTES',
            14,
            '#6b6b85',
            { roughness: 0 },
        ));
        config.commentary_bullets.forEach((b, i) => {
            elements.push(text(
                uid('bullet', i),
                crX, cbY + 24 + i * 22,
                `▸ ${b}`,
                11,
                '#505068',
                { roughness: 0 },
            ));
        });
    }
}

/* ═══════════════════════════════════════════════════════
   RATING SCALE GENERATOR
   ═══════════════════════════════════════════════════════
   Layout matches the "Clavicular" screenshot:

    LEFT SIDE                      CENTER             RIGHT SIDE
    ┌───────────┐                                    ┌─────┐
    │ HEADLINE  │                                    │ IMG │ 8  Premium
    └───────────┘                                    ├─────┤
    ┌───────────┐                   (video           │ IMG │ 7  Upper
    │  SUBJECT  │                    overlay          ├─────┤    Marginal
    │  IMAGE    │                    area)            │ IMG │ 6
    │  280x280  │                                    ├─────┤
    └───────────┘                                    │ IMG │ 5  Marginal
     Pros                                            ├─────┤
     • bullet                                        │ IMG │ 4  Sub
     • bullet                                        ├─────┤    Marginal
     Cons                                            │ IMG │ 3  Junk
     • bullet                                        └─────┘
     • bullet
   ═══════════════════════════════════════════════════════ */

const RATING_LEVELS = [
    { score: 8, label: 'Premium', scoreColor: '#2dd4bf', bg: '#1a3a2f', stroke: '#2dd4bf' },
    { score: 7, label: 'Upper', scoreColor: '#a7f3d0', bg: '#1a2f2a', stroke: '#2f9e44' },
    { score: 6, label: 'Marginal', scoreColor: '#FFEB3B', bg: '#2a2a1a', stroke: '#f59f00' },
    { score: 5, label: 'Marginal', scoreColor: '#fbbf24', bg: '#2a241a', stroke: '#f08c00' },
    { score: 4, label: 'Sub', scoreColor: '#FF9800', bg: '#2a1a1a', stroke: '#e8590c' },
    { score: 3, label: 'Junk', scoreColor: '#F44336', bg: '#2a1414', stroke: '#e03131' },
];

function generateRatingScale(config, elements) {
    // ─── RIGHT SIDE: Rating Scale ─────────────────
    const scaleX = 850;
    const scaleY = 60;
    const imgSize = 90;
    const scoreNumSize = 56;
    const rowGap = 12;
    const rowH = imgSize + rowGap;

    // Vertical bracket line
    elements.push({
        type: 'line',
        id: uid('scale-line', 0),
        x: scaleX + imgSize + 70,
        y: scaleY + 10,
        width: 0,
        height: RATING_LEVELS.length * rowH - rowGap - 20,
        points: [[0, 0], [0, RATING_LEVELS.length * rowH - rowGap - 20]],
        strokeColor: '#444466',
        backgroundColor: 'transparent',
        startArrowhead: null,
        endArrowhead: null,
        ...baseProps({ roughness: 0, strokeWidth: 2, opacity: 40 }),
    });

    RATING_LEVELS.forEach((level, i) => {
        const y = scaleY + i * rowH;

        // Reference image placeholder
        elements.push(rect(
            uid('ref-img', i),
            scaleX, y, imgSize, imgSize,
            level.bg, level.stroke,
            { roughness: 1 },
        ));

        // Placeholder icon
        elements.push(text(
            uid('ref-icon', i),
            scaleX + imgSize / 2 - 12, y + imgSize / 2 - 14,
            '👤',
            24,
            '#6b6b85',
            { textAlign: 'center' },
        ));

        // Large score number
        elements.push(text(
            uid('score-num', i),
            scaleX + imgSize + 14, y + 8,
            `${level.score}`,
            scoreNumSize,
            level.scoreColor,
        ));

        // Tier label
        elements.push(text(
            uid('tier-label', i),
            scaleX + imgSize + 90, y + 20,
            level.label,
            18,
            '#a0a0b8',
        ));

        // Two-word tier names
        if (level.score === 7) {
            elements.push(text(uid('tier-sub', 70 + i), scaleX + imgSize + 90, y + 44, 'Marginal', 18, '#a0a0b8'));
        }
        if (level.score === 4) {
            elements.push(text(uid('tier-sub', 40 + i), scaleX + imgSize + 90, y + 44, 'Marginal', 18, '#a0a0b8'));
        }
    });

    // ─── LEFT SIDE: Subject Panel ─────────────────
    const panelX = 60;
    const panelY = 40;

    // Subject headline
    elements.push(text(
        uid('subject-headline', 0),
        panelX, panelY,
        config.rating_subject || config.title || 'Subject',
        36,
        '#f0f0f5',
    ));

    // Subject image placeholder
    const subImgY = panelY + 60;
    const subImgSize = 280;

    elements.push(rect(
        uid('subject-img', 0),
        panelX, subImgY, subImgSize, subImgSize,
        '#1a1a24', '#33334d',
        { roughness: 1 },
    ));

    elements.push(text(
        uid('subject-img-icon', 0),
        panelX + subImgSize / 2 - 20, subImgY + subImgSize / 2 - 20,
        '📷',
        36,
        '#444466',
        { textAlign: 'center' },
    ));

    elements.push(text(
        uid('subject-img-label', 0),
        panelX + 20, subImgY + subImgSize - 30,
        'Drop subject image here',
        12,
        '#444466',
    ));

    // ─── PROS (green) ────────────────────────────
    const prosY = subImgY + subImgSize + 30;

    elements.push(text(
        uid('pros-label', 0),
        panelX, prosY,
        'Pros',
        22,
        '#2dd4bf',
    ));

    const pros = config.pros || ['Add positive metric...', 'Add positive metric...'];
    pros.forEach((p, i) => {
        elements.push(text(
            uid('pros-bullet', i),
            panelX + 8, prosY + 34 + i * 28,
            `•  ${p}`,
            15,
            '#2dd4bf',
        ));
    });

    // ─── CONS (red) ──────────────────────────────
    const consY = prosY + 34 + pros.length * 28 + 20;

    elements.push(text(
        uid('cons-label', 0),
        panelX, consY,
        'Cons',
        22,
        '#F44336',
    ));

    const cons = config.cons || ['Add negative metric...', 'Add negative metric...'];
    cons.forEach((c, i) => {
        elements.push(text(
            uid('cons-bullet', i),
            panelX + 8, consY + 34 + i * 28,
            `•  ${c}`,
            15,
            '#F44336',
        ));
    });

    // ─── Commentary ──────────────────────────────
    if (config.commentary_bullets?.length) {
        const commentY = consY + 34 + cons.length * 28 + 30;
        config.commentary_bullets.forEach((b, i) => {
            elements.push(text(
                uid('comment', i),
                panelX, commentY + i * 26,
                `▸ ${b}`,
                12,
                '#6b6b85',
            ));
        });
    }
}
