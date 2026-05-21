import React from 'react';

export default function CmfStatusCard({ status, eta }: { status: string, eta?: number }) {
    return (
        <div>
            <h3>Deployment Status</h3>
            <p>Status: {status}</p>
            {eta && <p>ETA: {eta} minutes</p>}
        </div>
    );
}
