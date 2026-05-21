import { SoloRecordingViewState } from './types';

export const initialState: SoloRecordingViewState = {
    phase: "brief",
    elapsed_seconds: 0,
    max_duration_seconds: 300,
    upload_ticket: "",
    upload_status: "not_started",
    stream_status: "connected"
};
