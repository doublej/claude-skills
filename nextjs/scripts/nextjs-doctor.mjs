#!/usr/bin/env node
/**
 * Next.js repo pattern audit
 * Run: node scripts/nextjs-doctor.mjs [path]
 */
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";

const IGNORED_DIRS = new Set([
  "node_modules", ".git", "dist", "build", ".next", ".turbo",
  ".cache", "coverage", ".output", ".vercel"
]);

const CODE_EXTS = new Set([".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"]);

async function exists(p) {
  try { await fsp.access(p); return true; } catch { return false; }
}

async function readJson(p) {
  return JSON.parse(await fsp.readFile(p, "utf8"));
}

async function findRepoRoot(startDir) {
  const resolved = path.resolve(startDir);
  if (await exists(path.join(resolved, "package.json"))) return resolved;
  try {
    const { execSync } = await import("node:child_process");
    const gitRoot = execSync("git rev-parse --show-toplevel", {
      cwd: resolved, encoding: "utf8", stdio: ["pipe", "pipe", "pipe"]
    }).trim();
    if (await exists(path.join(gitRoot, "package.json"))) return gitRoot;
  } catch { /* not a git repo */ }
  let dir = resolved;
  for (let i = 0; i < 3; i++) {
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
    if (await exists(path.join(dir, "package.json"))) return dir;
  }
  return resolved;
}

async function walk(dir, onFile) {
  let entries;
  try {
    entries = await fsp.readdir(dir, { withFileTypes: true });
  } catch (err) {
    if (err.code === "EACCES") return;
    throw err;
  }
  for (const ent of entries) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory() && !IGNORED_DIRS.has(ent.name)) await walk(p, onFile);
    else if (ent.isFile() && CODE_EXTS.has(path.extname(p))) await onFile(p);
  }
}

function countMatches(text, re) {
  return (text.match(re) || []).length;
}

function findMatches(text, re, filePath) {
  const results = [];
  const lines = text.split("\n");
  for (let i = 0; i < lines.length; i++) {
    if (re.test(lines[i])) {
      results.push({ file: filePath, line: i + 1, text: lines[i].trim() });
    }
  }
  return results;
}

async function main() {
  const repoRoot = await findRepoRoot(process.argv[2] || process.cwd());
  console.log(`\n🔍 Scanning: ${repoRoot}\n`);

  const pkgPath = path.join(repoRoot, "package.json");
  let pkg = null;
  if (await exists(pkgPath)) pkg = await readJson(pkgPath);

  // Detect Next.js version
  let nextVersion = null;
  const nextPkgPath = path.join(repoRoot, "node_modules/next/package.json");
  if (await exists(nextPkgPath)) {
    nextVersion = (await readJson(nextPkgPath)).version;
  } else if (pkg) {
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.next) nextVersion = deps.next;
  }

  if (!nextVersion) {
    console.log("❌ Next.js not found in this project");
    process.exitCode = 1;
    return;
  }

  // Detect config
  const deps = pkg ? { ...pkg.dependencies, ...pkg.devDependencies } : {};
  const features = [];
  if (deps.tailwindcss) features.push("Tailwind");
  if (deps.prisma || deps["@prisma/client"]) features.push("Prisma");
  if (deps.drizzle || deps["drizzle-orm"]) features.push("Drizzle");
  if (deps.zustand) features.push("Zustand");
  if (deps.swr) features.push("SWR");
  if (deps["@tanstack/react-query"]) features.push("React Query");

  // Check for cache components
  let cacheComponentsEnabled = false;
  for (const configFile of ["next.config.ts", "next.config.js", "next.config.mjs"]) {
    const configPath = path.join(repoRoot, configFile);
    if (await exists(configPath)) {
      const configText = await fsp.readFile(configPath, "utf8");
      if (configText.includes("cacheComponents")) {
        cacheComponentsEnabled = configText.includes("cacheComponents: true") ||
                                  configText.includes("cacheComponents:true");
      }
    }
  }

  // Check for app directory
  const hasAppDir = await exists(path.join(repoRoot, "app")) ||
                    await exists(path.join(repoRoot, "src/app"));
  const hasPagesDir = await exists(path.join(repoRoot, "pages")) ||
                      await exists(path.join(repoRoot, "src/pages"));

  // Scan code
  const stats = {
    files: 0,
    useClient: 0,
    useServer: 0,
    useCache: 0,
    useEffect: 0,
    useEffectFetch: 0,
    useStateFetch: 0,
    serverActions: 0,
    suspense: 0,
    dynamicImport: 0,
    revalidatePath: 0,
    revalidateTag: 0,
    nextImage: 0,
    htmlImg: 0,
    nextLink: 0,
    anchorTag: 0,
    barrelImports: 0,
    serverOnly: 0,
  };
  const warnings = [];

  await walk(repoRoot, async (filePath) => {
    const text = await fsp.readFile(filePath, "utf8");
    const rel = path.relative(repoRoot, filePath);
    stats.files++;

    stats.useClient += countMatches(text, /['"]use client['"]/g);
    stats.useServer += countMatches(text, /['"]use server['"]/g);
    stats.useCache += countMatches(text, /['"]use cache['"]/g);
    stats.useEffect += countMatches(text, /useEffect\s*\(/g);
    stats.suspense += countMatches(text, /<Suspense/g);
    stats.dynamicImport += countMatches(text, /dynamic\s*\(\s*\(\)/g);
    stats.revalidatePath += countMatches(text, /revalidatePath\s*\(/g);
    stats.revalidateTag += countMatches(text, /revalidateTag\s*\(/g);
    stats.nextImage += countMatches(text, /from ['"]next\/image['"]/g);
    stats.htmlImg += countMatches(text, /<img\s/g);
    stats.nextLink += countMatches(text, /from ['"]next\/link['"]/g);
    stats.anchorTag += countMatches(text, /<a\s+href=/g);
    stats.serverOnly += countMatches(text, /import ['"]server-only['"]/g);

    // Detect useEffect fetch anti-pattern
    if (/useEffect/.test(text) && /fetch\s*\(/.test(text) && /['"]use client['"]/.test(text)) {
      stats.useEffectFetch++;
      warnings.push(`⚠️  ${rel}: useEffect + fetch detected — consider Server Component`);
    }

    // Detect useState + fetch pattern
    if (/useState/.test(text) && /fetch\s*\(/.test(text) && /setLoading|setData|setError/.test(text)) {
      stats.useStateFetch++;
    }

    // Detect barrel imports from @/components
    const barrelMatches = findMatches(text, /from ['"]@\/components['"]/, filePath);
    if (barrelMatches.length > 0) {
      stats.barrelImports += barrelMatches.length;
      warnings.push(`⚠️  ${rel}:${barrelMatches[0].line}: barrel import from @/components — import directly`);
    }

    // Detect <img> without next/image
    if (/<img\s/.test(text) && !/eslint-disable/.test(text)) {
      const imgMatches = findMatches(text, /<img\s/, filePath);
      if (imgMatches.length > 0) {
        warnings.push(`⚠️  ${rel}:${imgMatches[0].line}: <img> tag — use next/image for optimization`);
      }
    }
  });

  // Report
  console.log("📦 Setup");
  console.log(`   Next.js: ${nextVersion}`);
  console.log(`   Router: ${hasAppDir ? "App Router" : ""}${hasPagesDir ? (hasAppDir ? " + Pages Router" : "Pages Router") : ""}`);
  console.log(`   Cache Components: ${cacheComponentsEnabled ? "✅ enabled" : "not enabled"}`);
  console.log(`   Libraries: ${features.join(", ") || "none detected"}`);
  console.log(`   Files scanned: ${stats.files}`);

  console.log("\n🏗️  Component Boundaries");
  console.log(`   'use client': ${stats.useClient}`);
  console.log(`   'use server': ${stats.useServer}`);
  console.log(`   'use cache': ${stats.useCache}`);
  console.log(`   server-only imports: ${stats.serverOnly}`);
  const clientRatio = stats.files > 0 ? ((stats.useClient / stats.files) * 100).toFixed(0) : 0;
  if (+clientRatio > 50) {
    console.log(`   ⚠️  ${clientRatio}% of files are client components — review if all need interactivity`);
  }

  console.log("\n📡 Data Fetching");
  console.log(`   useEffect: ${stats.useEffect}`);
  if (stats.useEffectFetch > 0) {
    console.log(`   ⚠️  useEffect+fetch: ${stats.useEffectFetch} files — migrate to Server Components`);
  }
  if (stats.useStateFetch > 0) {
    console.log(`   ⚠️  useState+fetch pattern: ${stats.useStateFetch} files — consider server-side fetching`);
  }
  console.log(`   <Suspense>: ${stats.suspense}`);
  console.log(`   dynamic(): ${stats.dynamicImport}`);
  console.log(`   revalidatePath: ${stats.revalidatePath}`);
  console.log(`   revalidateTag: ${stats.revalidateTag}`);

  console.log("\n🖼️  Assets");
  if (stats.htmlImg > 0) {
    console.log(`   ⚠️  <img> tags: ${stats.htmlImg} — use next/image for optimization`);
  } else {
    console.log(`   ✅ All images use next/image`);
  }
  console.log(`   next/image imports: ${stats.nextImage}`);

  console.log("\n🔗 Navigation");
  if (stats.anchorTag > 0) {
    console.log(`   ⚠️  <a href> tags: ${stats.anchorTag} — use next/link for client navigation`);
  }
  console.log(`   next/link imports: ${stats.nextLink}`);

  if (stats.barrelImports > 0) {
    console.log(`\n📦 Bundle`);
    console.log(`   ⚠️  Barrel imports: ${stats.barrelImports} — import directly from source files`);
  }

  if (warnings.length > 0) {
    console.log(`\n⚠️  Warnings (${warnings.length})`);
    for (const w of warnings.slice(0, 20)) console.log(`   ${w}`);
    if (warnings.length > 20) console.log(`   ... and ${warnings.length - 20} more`);
  } else {
    console.log("\n✅ No anti-patterns detected");
  }

  console.log("\n");
}

main().catch((err) => { console.error(err); process.exitCode = 1; });
