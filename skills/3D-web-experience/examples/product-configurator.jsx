import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF, OrbitControls, ContactShadows, Environment } from '@react-three/drei';

const COLORS = {
    red: '#C0392B',
    blue: '#2980B9',
    black: '#1A1A1A',
};

function ConfigurableProduct({ selectedColor }) {
    const { scene } = useGLTF('/product.glb'); // Ensure you run gltf-transform first

    useEffect(() => {
        scene.traverse((child) => {
            // Find the specific mesh to change color
            if (child.isMesh && child.name === 'body') {
                // Clone material to avoid shared material mutation across instances
                child.material = child.material.clone();
                child.material.color.set(COLORS[selectedColor]);
            }
        });
    }, [selectedColor, scene]);

    return <primitive object={scene} />;
}

export default function ProductConfigurator() {
    const [color, setColor] = useState('red');

    return (
        <div style={{ width: '100%', height: '500px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ padding: '10px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                {Object.keys(COLORS).map((c) => (
                    <button
                        key={c}
                        onClick={() => setColor(c)}
                        style={{
                            padding: '8px 16px', background: COLORS[c],
                            color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'
                        }}
                    >
                        {c.toUpperCase()}
                    </button>
                ))}
            </div>

            <div style={{ flex: 1, position: 'relative' }}>
                <Canvas
                    camera={{ position: [0, 0, 5], fov: 45 }}
                    dpr={[1, 2]} // Cap pixel ratio for mobile perf
                    frameloop="demand" // Render only when interaction happens
                    role="img"
                    aria-label="Interactive 3D product configurator"
                >
                    <ambientLight intensity={0.5} />
                    <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />

                    <React.Suspense fallback={null}>
                        <ConfigurableProduct selectedColor={color} />
                        <Environment preset="city" />
                        <ContactShadows position={[0, -1, 0]} opacity={0.4} scale={10} blur={2} />
                    </React.Suspense>

                    <OrbitControls enablePan={false} enableZoom={true} />
                </Canvas>
            </div>
        </div>
    );
}

useGLTF.preload('/product.glb');
