import { VideoRect } from './types';

export function isIntersection(r1: VideoRect, r2: VideoRect): boolean {
    return !(
        r2.x >= r1.x + r1.width ||
        r2.x + r2.width <= r1.x ||
        r2.y >= r1.y + r1.height ||
        r2.y + r2.height <= r1.y
    );
}

export function computeSafeGeometry(focal: VideoRect, candidate: VideoRect): VideoRect | null {
    if (!isIntersection(focal, candidate)) {
        return candidate;
    }
    return null; // indicates need for fallback to right drawer or defer
}
