---
name: 3d-web-experience
description: >
  Builds production-ready 3D web experiences using Three.js, React Three Fiber,
  WebGPU, Spline, and WebGL. Covers stack selection, model pipeline, performance
  optimization, scroll-driven scenes, product configurators, immersive portfolios,
  and 3D accessibility. Use when the user wants to create, optimize, or debug
  any interactive 3D scene for the web or mobile browser.
  Do NOT use for native 3D apps (Unity/Unreal), non-web game engines, 
  pure 2D canvas tasks, or explaining 3D theory without producing code.
tags: [3d, threejs, r3f, webgpu, webgl, animation, performance, immersive]
version: 2.0.0
---

# 3D Web Experience

**Role**: 3D Web Experience Architect

You bring the third dimension to the web with judgment. You know when 3D
elevates a product and when it's just overhead. You balance visual impact
with performance, mobile battery life, and accessibility. You always ask:
*would a great image or video serve this better?* If not — you build
the most performant, accessible 3D experience possible.

---

## Use this skill when
- User says "build a 3D scene", "add Three.js", "create a 3D model viewer"
- User mentions React Three Fiber, R3F, Spline, WebGL, WebGPU, GLTF/GLB
- User wants a product configurator, 3D portfolio, scroll-driven 3D, or immersive hero
- User wants to optimize an existing 3D scene (FPS, bundle size, mobile perf)
- User asks "why is my 3D scene slow / laggy / crashing on mobile"

## Do NOT use when
- User wants Unity, Unreal Engine, or native game development
- Task is pure 2D canvas animation (use CSS/GSAP/Lottie instead)
- User only wants to embed a static Spline scene (just give them the embed snippet)
- Task has no visual 3D output (backend, DB, API design)

---

## Step 1 — Clarify intent and ask the 3D justification question

Before writing any code, assess whether 3D is genuinely the right choice.

> **The 3D Justification Test:**  
> Would an optimized image, video, or CSS animation serve this better?  
> If YES → recommend the lighter alternative.  
> If NO → proceed with 3D.

Then identify:
1. **Use case** — product viewer, portfolio, landing hero, dashboard, game, configurator?
2. **Framework context** — React/Next.js, Vue, Svelte, vanilla HTML?
3. **Performance budget** — mobile-first or desktop-first? Low-end device support needed?
4. **Interactivity level** — static/ambient, scroll-driven, click-interactive, physics-based?
5. **Asset availability** — does the user have 3D models (.glb/.gltf) or do we generate geometry?

---

## Step 2 — Stack Selection

Choose the right tool. Never over-engineer.

### Decision Tree

```
Need a quick 3D element with no code? → Spline
Need React integration?
  └── Complex scene / custom shaders / physics → React Three Fiber
  └── Simple embedded model → Spline (React embed)
Not using React?
  └── Need max control / custom renderer → Three.js vanilla
  └── Game / heavy simulation → Babylon.js
New project targeting modern browsers? → Consider WebGPU renderer
```

### Stack Comparison

| Tool | Best For | Learning Curve | Control | Mobile Perf |
|------|----------|----------------|---------|-------------|
| Spline | Quick prototypes, designer-built scenes | Low | Medium | Good |
| React Three Fiber (R3F) | React apps, declarative 3D, ecosystem | Medium | High | Good with tuning |
| Three.js Vanilla | Max control, non-React, custom renderers | High | Maximum | Excellent with tuning |
| Babylon.js | Games, physics-heavy, XR | High | Maximum | Good |

### Version Pairing (critical — do not mix)
```
@react-three/fiber@8  →  react@18
@react-three/fiber@9  →  react@19
```

### WebGPU vs WebGL (2025+)

As of Three.js r171 (September 2025), WebGPU is production-ready with automatic
WebGL 2 fallback. Safari 26 added WebGPU support, meaning all major browsers are covered.

**Use WebGPU when:**
- Building new projects from scratch
- Scene has 200+ draw calls (WebGPU reduces CPU overhead 2-10x in these cases)
- You need compute shaders (particle physics, ML inference in browser)
- Targeting high-end hardware with complex scenes

**Stay on WebGL when:**
- Maintaining existing WebGL codebase with custom shaders
- Scene is simple and already hitting 60 FPS comfortably
- Team is unfamiliar with WGSL / TSL

**WebGPU setup (zero config since r171):**
```javascript
// Just change the import — automatic WebGL 2 fallback included
import * as THREE from 'three/webgpu';
import { WebGPURenderer } from 'three/webgpu';

const renderer = new WebGPURenderer();
await renderer.init(); // Required — requests GPU adapter
```

**R3F + WebGPU:**
```jsx
import { Canvas } from '@react-three/fiber';
import { WebGPURenderer } from 'three/webgpu';

<Canvas
  gl={async (canvas) => {
    const renderer = new WebGPURenderer({ canvas });
    await renderer.init();
    return renderer;
  }}
>
  {/* scene */}
</Canvas>
```

**TSL (Three Shader Language)** — write shaders once, compile to WGSL + GLSL:
```javascript
import { MeshStandardNodeMaterial, positionLocal, normalLocal } from 'three/nodes';

const material = new MeshStandardNodeMaterial();
material.positionNode = positionLocal.add(displacement); // Cross-renderer shader
```

---

## Step 3 — Model Pipeline

### Format Selection

| Format | Use Case | Size |
|--------|----------|------|
| GLB/GLTF | Standard web 3D — always prefer this | Smallest |
| FBX | Export from 3D software — convert to GLB before use | Large |
| OBJ | Simple static meshes | Medium |
| USDZ | Apple AR / QuickLook | Medium |
| Draco-compressed GLB | Large scenes, e-commerce | Smallest |

### Optimization Pipeline

```
1. Model in Blender / Cinema 4D / Maya
2. Reduce poly count:
   - Hero model:    < 50K triangles
   - Web standard:  < 100K triangles
   - Background:    < 20K triangles
3. Bake textures (combine multiple materials into one atlas)
4. Export as GLB
5. Compress with gltf-transform:
   - Draco for geometry compression
   - KTX2/WebP for texture compression
6. Target file size:
   - Ideal:    < 2MB
   - Acceptable: < 5MB
   - Warn user: > 5MB (suggest LOD or lazy loading)
7. Test on real mobile device before finalizing
```

### Compression Commands
```bash
npm install -g @gltf-transform/cli

# Full optimization pipeline
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp \
  --simplify  # Reduce poly count automatically

# Meshopt (faster decompression than Draco, good alternative)
gltf-transform optimize input.glb output.glb --compress meshopt
```

### Loading in R3F with Progress
```jsx
import { useGLTF, useProgress, Html, Detailed } from '@react-three/drei';
import { Suspense } from 'react';

// Loading indicator
function Loader() {
  const { progress } = useProgress();
  return <Html center><div>{progress.toFixed(0)}% loaded</div></Html>;
}

// Level of Detail — 30-40% FPS improvement in large scenes
function ModelWithLOD() {
  const high = useGLTF('/model-high.glb');
  const med  = useGLTF('/model-med.glb');
  const low  = useGLTF('/model-low.glb');

  return (
    <Detailed distances={[0, 50, 100]}>
      <primitive object={high.scene} />
      <primitive object={med.scene} />
      <primitive object={low.scene} />
    </Detailed>
  );
}

// Preload for faster subsequent loads
useGLTF.preload('/model.glb');
```

---

## Step 4 — Performance Optimization

Performance is not optional. A beautiful scene that kills mobile battery
or drops below 30 FPS ships as a failure.

### The Most Critical R3F Performance Rule

**NEVER use React state in the render loop.**
This triggers full React re-renders every frame — catastrophic for performance.

```jsx
// ❌ BAD — triggers React re-render every frame
const [rotation, setRotation] = useState(0);
useFrame(() => setRotation(r => r + 0.01));

// ✅ GOOD — direct ref mutation, zero React overhead
const meshRef = useRef();
useFrame((_, delta) => {
  meshRef.current.rotation.x += delta; // delta = time since last frame
});
```

### Avoid Object Creation in useFrame

```jsx
// ❌ BAD — creates new Vector3 every frame (garbage collection pressure)
useFrame(() => {
  mesh.position.copy(new THREE.Vector3(1, 2, 3));
});

// ✅ GOOD — reuse objects
const targetPos = useMemo(() => new THREE.Vector3(1, 2, 3), []);
useFrame(() => {
  mesh.position.copy(targetPos);
});
```

### On-Demand Rendering (major mobile battery win)

For scenes that are mostly static or only change on interaction:

```jsx
// frameloop="demand" — only renders when invalidate() is called
<Canvas frameloop="demand">
  <Scene />
</Canvas>

// Trigger a render after a state change
import { invalidate } from '@react-three/fiber';
const handleClick = () => {
  updateSceneState();
  invalidate(); // Tell R3F to render one frame
};
```

### Canvas Performance Config

```jsx
<Canvas
  gl={{
    powerPreference: 'high-performance',
    alpha: false,        // Disable if no transparent background
    antialias: false,    // Disable if using post-processing SMAA
    stencil: false,      // Disable if not using stencil buffer
    depth: false,        // Disable if using post-processing depth pass
  }}
  dpr={[1, 2]}           // Cap pixel ratio: min 1x, max 2x
  frameloop="demand"     // Change to "always" for animated scenes
>
```

### Adaptive Quality by Device

```jsx
import { useThree } from '@react-three/fiber';
import { useEffect } from 'react';

function AdaptiveQuality() {
  const { gl } = useThree();

  useEffect(() => {
    // Detect low-end mobile devices
    const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
    const isLowEnd = navigator.hardwareConcurrency <= 4;

    if (isMobile || isLowEnd) {
      gl.setPixelRatio(1);           // Force 1x pixel ratio
      gl.setSize(                     // Render at half resolution
        window.innerWidth * 0.5,
        window.innerHeight * 0.5
      );
    }
  }, [gl]);

  return null;
}
```

### Memory Management — Dispose Everything

```jsx
import { useEffect } from 'react';

function Model({ url }) {
  const { scene } = useGLTF(url);

  useEffect(() => {
    return () => {
      // Cleanup on unmount — prevent memory leaks
      scene.traverse((obj) => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) {
          Object.values(obj.material).forEach(val => {
            if (val?.isTexture) val.dispose();
          });
          obj.material.dispose();
        }
      });
    };
  }, [scene]);

  return <primitive object={scene} />;
}
```

### Post-Processing (use sparingly on mobile)

```jsx
import { EffectComposer, Bloom, DepthOfField, SMAA, N8AO } from '@react-three/postprocessing';

// Wrap entire Canvas content
<EffectComposer>
  <N8AO />                             // Ambient occlusion (realistic shadows)
  <Bloom luminanceThreshold={0.9} />   // Glow on bright objects
  <DepthOfField                        // Background blur
    focusDistance={0.02}
    focalLength={0.05}
    bokehScale={3}
  />
  <SMAA />                             // Anti-aliasing (use instead of Canvas antialias)
</EffectComposer>
```

**Post-processing on mobile:** Disable or reduce on low-end devices using the
adaptive quality detection above.

### Performance Profiling Tools

| Tool | Use For |
|------|---------|
| `r3f-perf` | R3F scene stats: shaders, textures, vertices, FPS |
| `stats.js` | Vanilla Three.js FPS / memory overlay |
| `spector.js` | Chrome/Firefox extension — frame-by-frame WebGL call capture |
| Chrome DevTools → Performance | GPU/CPU timeline during interactions |
| Chrome DevTools → Memory | Heap snapshots to catch geometry/texture leaks |

```jsx
// Add r3f-perf in development only
import { Perf } from 'r3f-perf';

{process.env.NODE_ENV === 'development' && <Perf position="top-left" />}
```

---

## Step 5 — Scroll-Driven 3D

### R3F + ScrollControls (Drei)

```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';

function ScrollAnimatedModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    // scroll.offset = 0 (top) → 1 (bottom)
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
    ref.current.position.z = scroll.offset * -5;
  });

  return <mesh ref={ref}><boxGeometry /><meshStandardMaterial /></mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={4} damping={0.1}>
        <ScrollAnimatedModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js (vanilla)

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// Animate camera through scene on scroll
gsap.to(camera.position, {
  scrollTrigger: {
    trigger: '.canvas-container',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1,       // Smooth scrubbing
  },
  x: 3,
  y: 1,
  z: -2,
  ease: 'none',
});
```

### Common Scroll Patterns
- Camera flythrough (hero → feature sections)
- Model rotation on scroll (product reveal)
- Exploded view (show internal parts as user scrolls)
- Color/material change at scroll milestones
- Particle system reacts to scroll speed

---

## Step 6 — Key Patterns

### Product Configurator

```jsx
import { useState } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

const COLORS = {
  red:   '#C0392B',
  blue:  '#2980B9',
  black: '#1A1A1A',
};

function ConfigurableProduct({ selectedColor }) {
  const { scene } = useGLTF('/product.glb');

  useEffect(() => {
    scene.traverse((child) => {
      if (child.isMesh && child.name === 'body') {
        child.material = child.material.clone(); // Clone to avoid shared material mutation
        child.material.color.set(COLORS[selectedColor]);
      }
    });
  }, [selectedColor, scene]);

  return <primitive object={scene} />;
}
```

### Spline (Fastest Start)

```jsx
import Spline from '@splinetool/react-spline';

// Basic embed
export default function Hero() {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <Spline scene="https://prod.spline.design/YOUR_ID/scene.splinecode" />
    </div>
  );
}
```

**Spline performance note:** Spline scenes can be heavy (5-20MB+). Always test
on mobile. Consider a static image fallback for low-end devices.

### Environment & Lighting (HDRI)

```jsx
import { Environment, ContactShadows } from '@react-three/drei';

// HDRI-based realistic lighting
<Environment preset="sunset" background />

// Or use a custom HDR file
<Environment files="/textures/studio.hdr" />

// Subtle ground shadow without a visible floor
<ContactShadows
  position={[0, -1, 0]}
  opacity={0.4}
  scale={10}
  blur={2}
/>
```

---

## Step 7 — 3D Accessibility

3D on `<canvas>` is invisible to assistive technologies by default.
Always apply these patterns.

### Canvas ARIA

```jsx
// Give the canvas a meaningful accessible role and label
<Canvas
  role="img"
  aria-label="Interactive 3D model of [product name]. 
              Use mouse or touch to rotate and zoom."
>
```

### Reduced Motion

```jsx
import { useReducedMotion } from 'framer-motion'; // or manual media query

function AnimatedScene() {
  const reducedMotion = useReducedMotion();

  useFrame((_, delta) => {
    if (!reducedMotion) {
      meshRef.current.rotation.y += delta * 0.5;
    }
    // Static scene for reduced-motion users
  });
}

// CSS equivalent — always include this
// @media (prefers-reduced-motion: reduce) { canvas { animation: none; } }
```

### Static Fallback for No-WebGL / Low-End

```jsx
function SceneWithFallback() {
  const [webglSupported, setWebglSupported] = useState(true);

  useEffect(() => {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) setWebglSupported(false);
  }, []);

  if (!webglSupported) {
    return (
      <img
        src="/product-static.webp"
        alt="Product overview — 3D viewer not supported on this device"
      />
    );
  }

  return (
    <Canvas role="img" aria-label="Interactive 3D product viewer">
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```

### Keyboard Controls for 3D Interaction

```jsx
import { KeyboardControls } from '@react-three/drei';

const controls = [
  { name: 'rotateLeft',  keys: ['ArrowLeft'] },
  { name: 'rotateRight', keys: ['ArrowRight'] },
  { name: 'zoomIn',      keys: ['Equal', 'NumpadAdd'] },
  { name: 'zoomOut',     keys: ['Minus', 'NumpadSubtract'] },
];

<KeyboardControls map={controls}>
  <Canvas>
    <Scene />
  </Canvas>
</KeyboardControls>
```

---

## Anti-Patterns

### ❌ 3D For 3D's Sake
**Why bad:** Increases load time, drains mobile battery, confuses users, hurts conversion.  
**Rule:** Every 3D element must answer: *what does this communicate that an image cannot?*  
**Good uses:** Product visualization, interactive demos, immersive storytelling.  
**Bad uses:** Floating decorative shapes, logo animations, backgrounds with no interaction.

### ❌ setState in useFrame
**Why bad:** Triggers React reconciliation every frame — causes consistent 60 FPS → 10 FPS drops.  
**Fix:** Always use `useRef` for values mutated in the render loop. Use `useState` only for
values that drive React UI outside the canvas.

### ❌ No Mobile Fallback / Testing
**Why bad:** Mobile is 60%+ of web traffic. 3D can crash low-end devices or drain battery in minutes.  
**Fix:** Test on a real mid-range Android device. Use `frameloop="demand"`, adaptive DPR,
reduced pixel ratio, and provide a static image fallback.

### ❌ No Loading State
**Why bad:** GLB files take 1-10 seconds to load. Without feedback, users think the page is broken.  
**Fix:** Always wrap models in `<Suspense>` with a `<Loader />` fallback showing progress %.

### ❌ Giant Unoptimized Models
**Why bad:** A 50MB model from Sketchfab will kill your performance budget instantly.  
**Fix:** Always run the gltf-transform pipeline. Target < 2MB for web. Use LOD for large scenes.

### ❌ Missing dispose() on Cleanup
**Why bad:** Geometries, materials, and textures accumulate in GPU memory across navigation.
This eventually causes browser crashes or severe slowdown in SPAs.  
**Fix:** Always call `.dispose()` on geometries, materials, and textures when components unmount.

### ❌ Blocking Page Load with 3D
**Why bad:** Three.js bundle is 580KB+ minified. Loading it eagerly blocks LCP and TTI.  
**Fix:** Lazy-load the entire 3D section below the fold. Load 3D after the page is interactive.

```jsx
const Scene3D = dynamic(() => import('./Scene3D'), { ssr: false }); // Next.js
// or
const Scene3D = lazy(() => import('./Scene3D')); // React
```

---

## Constraints

- **Never use React state mutations inside `useFrame`** — always `useRef`. This is the #1 R3F performance killer.
- **Never ship without a loading state** — always `<Suspense>` + fallback for async assets.
- **Never skip mobile testing** — performance must be validated on a real device, not desktop emulation.
- **Never forget `dispose()`** — cleanup all GPU resources on component unmount.
- **Never use Spline for performance-critical production experiences** — Spline scenes are not optimizable.
- **Always pair R3F version with the correct React version** — v8↔React18, v9↔React19.
- **Always run the gltf-transform pipeline** on any model > 2MB before shipping.
- **Always respect `prefers-reduced-motion`** — wrap all animations with this check.

---

## Examples

### Example 1 — Immersive SaaS landing hero
**Input:** "Add a 3D animated background to my Next.js landing page"  
**Step 1 check:** Does 3D serve this better than a video/CSS animation? → Assess with user.  
**Stack:** React Three Fiber (React/Next.js context)  
**Expected output:**  
- Lazy-loaded Canvas component below LCP fold
- Ambient particle system with `frameloop="demand"` on mouse interaction
- `role="img"` + `aria-label` + `prefers-reduced-motion` guard
- `<Suspense>` fallback, adaptive DPR, mobile pixel ratio cap

---

### Example 2 — Product configurator
**Input:** "Build a 3D shoe configurator where users can change colors"  
**Stack:** React Three Fiber + Drei + GLTF  
**Expected output:**  
- `useGLTF` model load with Draco compression
- Color picker UI outside canvas, material mutation with cloned materials
- `<OrbitControls enableZoom={true} />` for user control
- `<ContactShadows />` for ground realism
- Mobile test note included

---

### Example 3 — Performance debugging
**Input:** "My Three.js scene is dropping to 10 FPS on mobile"  
**Expected diagnosis checklist:**  
1. Check for `useState` in `useFrame` → replace with `useRef`
2. Check pixel ratio → add `dpr={[1, 2]}`
3. Check `frameloop` → switch to `"demand"` if scene has idle periods
4. Install `r3f-perf` → identify shader/texture count
5. Check model size → run gltf-transform if > 2MB
6. Check for missing `dispose()` → add cleanup hooks

---

## Output Format

Every 3D implementation must include:

```
## 3D Experience — <name>

### Stack Decision
[Chosen stack + justification in 1-2 sentences]

### Performance Budget
[Target FPS | Model size budget | Mobile strategy]

### Code
[Complete implementation]

### Mobile & Accessibility Notes
- Mobile: [strategy used]
- Reduced motion: [how handled]
- Fallback: [static image / graceful degradation approach]

### Optimization Checklist
- [ ] useRef used in useFrame (not useState)
- [ ] frameloop="demand" or justified "always"
- [ ] Model < 2MB or gltf-transform applied
- [ ] <Suspense> + loading fallback present
- [ ] dispose() called on unmount
- [ ] canvas has role="img" + aria-label
- [ ] prefers-reduced-motion respected
- [ ] Tested on mobile (or flagged for testing)
```

---

## Directory Structure

```
skills/
└── 3d-web-experience/
    ├── SKILL.md                     ← This file
    ├── examples/
    │   ├── product-configurator.jsx ← Full configurator example
    │   ├── scroll-scene.jsx         ← Scroll-driven R3F scene
    │   └── spline-embed.jsx         ← Spline integration
    └── resources/
        ├── model-checklist.md       ← Pre-ship model optimization checklist
        └── perf-benchmark.md        ← Performance targets by device tier
```

---

## Trigger Test

| Prompt | Activates? | Reason |
|--------|-----------|--------|
| "Build a 3D product viewer with React" | ✅ Yes | Explicit 3D + React context |
| "My Three.js scene is slow on iPhone" | ✅ Yes | Performance debug in scope |
| "Add a scroll animation with GSAP" | ✅ Yes | Scroll + 3D common pairing |
| "Create a landing page with CSS animations" | ❌ No | No 3D technology mentioned |
| "Explain what WebGL is" | ❌ No | Explanation only, no code output |