# 3D Model Pre-Ship Optimization Checklist

Before shipping any 3D model (.glb/.gltf) to production, ensure it meets the following criteria. Unoptimized models will cause heavy battery drain, long initial pageloads, and sluggish frame rates on average mobile devices.

## 1. Geometry & Poly Count
- [ ] **Triangle count fits the performance budget:**
  - Background/Ambient models: `< 20K triangles`
  - Standard web products: `< 100K triangles`
  - High-end hero (desktop focused): `< 250K triangles max`
- [ ] Internal/unseen geometries are deleted.
- [ ] Level of Detail (LOD) models are generated for complex scenes extending deep into the background.

## 2. Textures & Materials
- [ ] Baked textures are used wherever possible (consolidate multiple materials into one texture atlas).
- [ ] Texture maps are correctly sized:
  - Base color / Albedo: `1024x1024` or `2048x2048` (only if detailed).
  - Normal/Roughness/Metalness: `512x512` usually suffices.
  - Never ship `4096x4096` textures to the web without aggressive texture compression.
- [ ] Unused materials are purged from the file.

## 3. Compression Pipeline (gltf-transform)
- [ ] Run `gltf-transform` to compress the final asset.
- [ ] Use Draco or Meshopt to compress geometry.
- [ ] Compress textures using WEBP or KTX2 format.

Example compression command:
```bash
gltf-transform optimize raw_model.glb optimized_model.glb \
  --compress draco \
  --texture-compress webp \
  --simplify
```

## 4. Final Delivery
- [ ] Final file size is `< 2MB` (ideal) or `< 5MB` (acceptable).
- [ ] The web application uses `<Suspense>` and a `<Loader>` while fetching the `.glb`.
- [ ] `useGLTF.preload('/optimized_model.glb')` is employed so assets are fetched ASAP.
