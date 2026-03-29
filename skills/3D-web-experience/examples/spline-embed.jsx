import React, { useState } from 'react';
import Spline from '@splinetool/react-spline';

export default function SplineEmbed() {
    const [isLoading, setIsLoading] = useState(true);

    // Called when the Spline scene is fully loaded
    const handleLoad = (splineApp) => {
        setIsLoading(false);
        // You can access the Spline app instance here to manipulate it
        // splineApp.setZoom(1.5);
    };

    return (
        <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
            {isLoading && (
                <div style={{
                    position: 'absolute', inset: 0, display: 'flex',
                    alignItems: 'center', justifyContent: 'center',
                    backgroundColor: '#f5f5f5', color: '#666'
                }}>
                    Loading 3D Experience...
                </div>
            )}

            {/* 
        Note: Spline scenes can be heavy (5-20MB+). 
        Monitor performance on mobile and provide image fallbacks for low-end devices if needed.
      */}
            <Spline
                scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
                onLoad={handleLoad}
            />
        </div>
    );
}
