#!/usr/bin/env node
/**
 * Three.js asset size audit
 * Run: node scripts/asset-audit.mjs [path]
 */
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";

const ASSET_EXTS = new Set([
  ".glb", ".gltf", ".fbx", ".obj",
  ".jpg", ".jpeg", ".png", ".webp", ".hdr", ".exr", ".ktx2",
  ".mp3", ".wav", ".ogg"
]);

const IGNORED_DIRS = new Set([
  "node_modules", ".git", "dist", "build", ".next"
]);

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

async function walk(dir, onFile) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const ent of entries) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory() && !IGNORED_DIRS.has(ent.name)) {
      await walk(p, onFile);
    } else if (ent.isFile() && ASSET_EXTS.has(path.extname(p).toLowerCase())) {
      const stat = await fsp.stat(p);
      await onFile(p, stat.size);
    }
  }
}

async function main() {
  const root = process.argv[2] || process.cwd();
  console.log(`\n📦 Scanning assets in: ${root}\n`);

  const assets = [];
  await walk(root, (filePath, size) => {
    assets.push({ path: filePath, size, ext: path.extname(filePath).toLowerCase() });
  });

  if (assets.length === 0) {
    console.log("No assets found.\n");
    return;
  }

  // Sort by size descending
  assets.sort((a, b) => b.size - a.size);

  // Group by type
  const byType = {};
  for (const a of assets) {
    const type = a.ext;
    if (!byType[type]) byType[type] = { count: 0, total: 0 };
    byType[type].count++;
    byType[type].total += a.size;
  }

  // Summary
  console.log("📊 Summary by Type");
  console.log("─".repeat(50));
  for (const [ext, data] of Object.entries(byType).sort((a, b) => b[1].total - a[1].total)) {
    console.log(`   ${ext.padEnd(8)} ${String(data.count).padStart(4)} files  ${formatSize(data.total).padStart(10)}`);
  }

  const totalSize = assets.reduce((sum, a) => sum + a.size, 0);
  console.log("─".repeat(50));
  console.log(`   Total: ${assets.length} files, ${formatSize(totalSize)}`);

  // Largest files
  console.log("\n🔝 Largest Files");
  console.log("─".repeat(70));
  for (const a of assets.slice(0, 15)) {
    const relPath = path.relative(root, a.path);
    console.log(`   ${formatSize(a.size).padStart(10)}  ${relPath}`);
  }

  // Warnings
  console.log("\n⚠️  Recommendations");
  console.log("─".repeat(50));

  const largeTextures = assets.filter(a =>
    [".jpg", ".jpeg", ".png", ".webp"].includes(a.ext) && a.size > 1024 * 1024
  );
  if (largeTextures.length > 0) {
    console.log(`   ${largeTextures.length} textures > 1MB - consider resizing or KTX2`);
  }

  const largeModels = assets.filter(a =>
    [".glb", ".gltf", ".fbx"].includes(a.ext) && a.size > 5 * 1024 * 1024
  );
  if (largeModels.length > 0) {
    console.log(`   ${largeModels.length} models > 5MB - consider DRACO/meshopt compression`);
  }

  const uncompressedTextures = assets.filter(a =>
    [".jpg", ".jpeg", ".png"].includes(a.ext)
  );
  const ktx2Count = assets.filter(a => a.ext === ".ktx2").length;
  if (uncompressedTextures.length > 5 && ktx2Count === 0) {
    console.log(`   ${uncompressedTextures.length} uncompressed textures - consider KTX2 for GPU compression`);
  }

  const hdrFiles = assets.filter(a => a.ext === ".hdr");
  if (hdrFiles.length > 1) {
    console.log(`   ${hdrFiles.length} HDR files - reuse environment maps when possible`);
  }

  console.log("\n");
}

main().catch(console.error);
