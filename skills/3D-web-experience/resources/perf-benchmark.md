# 3D Web Performance Benchmarks by Device Tier

Target 60 FPS (frames per second) universally, but gracefully degrade resolution, effects, or frame targets (30 FPS limit) on lower-end hardware to preserve battery and maintain interactive responsiveness.

## Device Tiers

### High-End (Desktop / Latest Flagships)
*e.g. M-series Macs, RTX GPUs, iPhone 14/15 Pro, Galaxy S23/S24*
- **Target FPS:** 60 - 120 FPS
- **Draw Calls:** Up to ~500 (WebGL 2) or ~2000+ (WebGPU)
- **Geometry:** 250K - 500K triangles
- **Post-Processing:** Bloom, Depth of Field, SMAA, Ambient Occlusion allowed
- **Resolution:** Full Native (`dpr=window.devicePixelRatio`)

### Mid-Range (Standard Mobile / Older Laptops)
*e.g. iPhone 11-13, standard modern Androids, Intel UHD integrated graphics*
- **Target FPS:** 60 FPS
- **Draw Calls:** < 150
- **Geometry:** < 100K triangles
- **Post-Processing:** Very limited (maybe one light SMAA or Bloom pass, disable AO)
- **Resolution:** Capped Pixel Ratio (`dpr={[1, 2]}`)

### Low-End (Budget Mobile / Power Saving Mode)
*e.g. Budget Androids, iPhone 8, 5+ year old laptops*
- **Target FPS:** 30 - 60 FPS
- **Draw Calls:** < 50
- **Geometry:** < 30K triangles
- **Post-Processing:** None.
- **Resolution:** Downscaled (`dpr={1}` or explicitly render at half resolution)
- *Consider falling back to a static image entirely.*

## Measurement & Auditing

1. **Use `r3f-perf` or `stats.js`** during development to monitor FPS and memory.
2. **Check GPU Memory Management:** Ensure `.dispose()` is called on all custom geometries, materials, and textures when the component unmounts.
3. **Audit React Re-renders:** Verify that `<Canvas>` wrapper components do NOT re-render on every frame. (Never use `useState` for frame-by-frame animation).
4. **Use Chrome DevTools (Performance Tab):** Record a 10s interaction and verify that the "GPU" bar isn't pegged at 100%. Check the "Main" thread for long tasks caused by React reconciliation.
