#!/usr/bin/env node
// manifest.mjs — Generate screenshot manifest with OCR, dimensions, contrast, colors
// Usage: node manifest.mjs <screenshots-dir>
// Deps: npm install tesseract.js sharp get-image-colors

import { readdir, writeFile } from 'fs/promises';
import { join, relative } from 'path';
import sharp from 'sharp';
import Tesseract from 'tesseract.js';
import getColors from 'get-image-colors';

const dir = process.argv[2];
if (!dir) { console.error('Usage: node manifest.mjs <screenshots-dir>'); process.exit(1); }

async function findPngs(base, sub = '') {
  const entries = await readdir(join(base, sub), { withFileTypes: true });
  const files = [];
  for (const e of entries) {
    const rel = join(sub, e.name);
    if (e.isDirectory()) files.push(...await findPngs(base, rel));
    else if (e.name.endsWith('.png')) files.push(rel);
  }
  return files;
}

function hexFromRgb(r, g, b) {
  return '#' + [r, g, b].map(c => c.toString(16).padStart(2, '0')).join('');
}

function luminance(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const toLinear = (c) => c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}

function contrastRatio(hex1, hex2) {
  const l1 = luminance(hex1), l2 = luminance(hex2);
  const lighter = Math.max(l1, l2), darker = Math.min(l1, l2);
  return +((lighter + 0.05) / (darker + 0.05)).toFixed(1);
}

async function analyzeImage(filepath) {
  const img = sharp(filepath);
  const { width, height, channels } = await img.metadata();
  const hasAlpha = channels === 4;

  // OCR
  const { data: { text } } = await Tesseract.recognize(filepath, 'eng');
  const ocr = text.trim();

  // Primary colors
  const colors = await getColors(filepath, { count: 5 });
  const primaryColors = colors.map(c => c.hex());

  // Contrast: ratio between lightest and darkest dominant color
  const sorted = [...primaryColors].sort((a, b) => luminance(a) - luminance(b));
  const contrast = sorted.length >= 2
    ? contrastRatio(sorted[sorted.length - 1], sorted[0])
    : 1;

  return { dimensions: { width, height }, ocr, contrast, primaryColors, hasAlpha };
}

const pngs = await findPngs(dir);
console.log(`Found ${pngs.length} PNG files`);

const screenshots = [];
for (const file of pngs) {
  const filepath = join(dir, file);
  process.stdout.write(`  ${file}...`);
  try {
    const info = await analyzeImage(filepath);
    screenshots.push({ file, ...info });
    console.log(' done');
  } catch (err) {
    console.log(` error: ${err.message}`);
  }
}

const manifest = { generated: new Date().toISOString(), screenshots };
const outPath = join(dir, 'manifest.json');
await writeFile(outPath, JSON.stringify(manifest, null, 2));
console.log(`\nManifest written to ${outPath}`);
