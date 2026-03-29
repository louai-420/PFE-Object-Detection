import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { ScrollControls, useScroll, useGLTF, Environment } from '@react-three/drei';

function ScrollAnimatedModel() {
    const scroll = useScroll();
    const ref = useRef();
    const { scene } = useGLTF('/model-optimized.glb');

    useFrame(() => {
        // scroll.offset goes from 0 (top) to 1 (bottom)
        const r = scroll.offset * Math.PI * 2;

        // Direct mutation - NEVER use React state in useFrame
        ref.current.rotation.y = r;
        ref.current.position.y = -scroll.offset * 2;
        ref.current.position.z = scroll.offset * -5;
    });

    return (
        <group ref={ref}>
            <primitive object={scene} />
        </group>
    );
}

export default function ScrollScene() {
    return (
        <div style={{ width: '100vw', height: '100vh', display: 'block' }}>
            <Canvas
                dpr={[1, 2]}
                camera={{ position: [0, 0, 5], fov: 45 }}
                role="img"
                aria-label="3D model that rotates as you scroll down the page"
            >
                <ambientLight intensity={0.5} />
                <directionalLight position={[10, 10, 5]} intensity={1} />

                <React.Suspense fallback={null}>
                    <Environment preset="city" />
                    {/* pages={3} means the scroll area is 3x the height of the container */}
                    <ScrollControls pages={3} damping={0.1}>
                        <ScrollAnimatedModel />
                    </ScrollControls>
                </React.Suspense>
            </Canvas>
        </div>
    );
}

useGLTF.preload('/model-optimized.glb');
