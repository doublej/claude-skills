#!/usr/bin/env node
/**
 * Three.js repo pattern audit
 * Run: node scripts/three-doctor.mjs [path]
 */
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";

const IGNORED_DIRS = new Set([
  "node_modules", ".git", "dist", "build", ".next", ".svelte-kit",
  ".turbo", ".cache", "coverage", ".nuxt", ".output"
]);

const CODE_EXTS = new Set([".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"]);

async function exists(p) {
  try { await fsp.access(p); return true; } catch { return false; }
}

async function readJson(p) {
  return JSON.parse(await fsp.readFile(p, "utf8"));
}

async function findRepoRoot(startDir) {
  let dir = path.resolve(startDir);
  for (let i = 0; i < 8; i++) {
    if (await exists(path.join(dir, "package.json"))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(startDir);
}

async function walk(dir, onFile) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const ent of entries) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory() && !IGNORED_DIRS.has(ent.name)) await walk(p, onFile);
    else if (ent.isFile() && CODE_EXTS.has(path.extname(p))) await onFile(p);
  }
}

function countMatches(text, re) {
  return (text.match(re) || []).length;
}

async function main() {
  const repoRoot = await findRepoRoot(process.argv[2] || process.cwd());
  console.log(`\n🔍 Scanning: ${repoRoot}\n`);

  // Read package.json
  const pkgPath = path.join(repoRoot, "package.json");
  let pkg = null;
  if (await exists(pkgPath)) pkg = await readJson(pkgPath);

  // Detect Three.js version
  let threeVersion = null;
  const threePkgPath = path.join(repoRoot, "node_modules/three/package.json");
  if (await exists(threePkgPath)) {
    threeVersion = (await readJson(threePkgPath)).version;
  } else if (pkg) {
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.three) threeVersion = deps.three;
  }

  // Detect frameworks
  const deps = pkg ? { ...pkg.dependencies, ...pkg.devDependencies } : {};
  const frameworks = [];
  if (deps["@react-three/fiber"]) frameworks.push("R3F");
  if (deps["@react-three/drei"]) frameworks.push("Drei");
  if (deps.next) frameworks.push("Next.js");
  if (deps.vite) frameworks.push("Vite");
  if (deps.vue || deps["@vue/core"]) frameworks.push("Vue");
  if (deps.svelte) frameworks.push("Svelte");

  // Scan code
  const stats = {
    files: 0,
    threeImports: 0,
    r3fImports: 0,
    legacyEncoding: 0,
    modernColorSpace: 0,
    effectComposer: 0,
    outputPass: 0,
    dispose: 0,
    requestAnimationFrame: 0,
    setAnimationLoop: 0,
    instancedMesh: 0,
    draco: 0,
    ktx2: 0,
    gltfLoader: 0,
    pmremGenerator: 0
  };

  await walk(repoRoot, async (filePath) => {
    const text = await fsp.readFile(filePath, "utf8");
    stats.files++;
    stats.threeImports += countMatches(text, /from ['"]three['"]/g);
    stats.r3fImports += countMatches(text, /@react-three\/fiber/g);
    stats.legacyEncoding += countMatches(text, /\.encoding\s*=/g);
    stats.modernColorSpace += countMatches(text, /\.colorSpace\s*=/g);
    stats.effectComposer += countMatches(text, /EffectComposer/g);
    stats.outputPass += countMatches(text, /OutputPass/g);
    stats.dispose += countMatches(text, /\.dispose\(\)/g);
    stats.requestAnimationFrame += countMatches(text, /requestAnimationFrame/g);
    stats.setAnimationLoop += countMatches(text, /setAnimationLoop/g);
    stats.instancedMesh += countMatches(text, /InstancedMesh/g);
    stats.draco += countMatches(text, /DRACOLoader/g);
    stats.ktx2 += countMatches(text, /KTX2Loader/g);
    stats.gltfLoader += countMatches(text, /GLTFLoader/g);
    stats.pmremGenerator += countMatches(text, /PMREMGenerator/g);
  });

  // Report
  console.log("📦 Setup");
  console.log(`   Three.js: ${threeVersion || "not found"}`);
  console.log(`   Frameworks: ${frameworks.join(", ") || "vanilla"}`);
  console.log(`   Files scanned: ${stats.files}`);

  console.log("\n🎨 Color Management");
  if (stats.legacyEncoding > 0 && stats.modernColorSpace > 0) {
    console.log(`   ⚠️  Mixed patterns: .encoding (${stats.legacyEncoding}) + .colorSpace (${stats.modernColorSpace})`);
  } else if (stats.legacyEncoding > 0) {
    console.log(`   ⚠️  Legacy .encoding found (${stats.legacyEncoding}) - consider migrating to .colorSpace`);
  } else if (stats.modernColorSpace > 0) {
    console.log(`   ✅ Using modern .colorSpace (${stats.modernColorSpace})`);
  }

  console.log("\n🎬 Postprocessing");
  if (stats.effectComposer > 0) {
    console.log(`   EffectComposer: ${stats.effectComposer} uses`);
    if (stats.outputPass === 0) {
      console.log(`   ⚠️  No OutputPass found - may cause double tone mapping`);
    } else {
      console.log(`   ✅ OutputPass: ${stats.outputPass} uses`);
    }
  } else {
    console.log(`   No EffectComposer detected`);
  }

  console.log("\n⚡ Performance");
  console.log(`   InstancedMesh: ${stats.instancedMesh}`);
  console.log(`   GLTFLoader: ${stats.gltfLoader}`);
  console.log(`   DRACO: ${stats.draco > 0 ? "✅" : "not used"}`);
  console.log(`   KTX2: ${stats.ktx2 > 0 ? "✅" : "not used"}`);

  console.log("\n🧹 Lifecycle");
  console.log(`   dispose() calls: ${stats.dispose}`);
  console.log(`   RAF: ${stats.requestAnimationFrame}, setAnimationLoop: ${stats.setAnimationLoop}`);
  if (stats.dispose === 0 && stats.threeImports > 0) {
    console.log(`   ⚠️  No dispose calls found - check for memory leaks`);
  }

  console.log("\n🌍 Environment");
  console.log(`   PMREMGenerator: ${stats.pmremGenerator > 0 ? "✅" : "not used"}`);

  console.log("\n");
}

main().catch(console.error);
