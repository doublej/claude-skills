#!/usr/bin/env bun
/* eslint-disable no-console */
import type { JsonArray, JsonObject, PullOptions, PushOptions } from './lib/types';
import { program } from 'commander';
import { config, type FileName } from './config';
import { diffObjects, mergeWithBlacklist } from './lib/merger';
import { exportToArraySheet, exportToKeyValue, getNestedValue, parseArraySheet, parseKeyValueSheet } from './lib/parser';
import { getBlacklistPatterns } from './lib/path-matcher';
import { createSheet, readSheet, sheetExists, writeSheet } from './lib/sheets';
import { validateContent } from './lib/validator';
import { formatChange, readJsonFile, writeJsonFile } from './lib/writer';

const fileNames = Object.keys(config.files) as FileName[];

function validateConfig(): void {
  if (!config.spreadsheetId) {
    console.error('Error: GOOGLE_SHEETS_ID environment variable not set');
    process.exit(1);
  }
}

async function pullFile(fileName: FileName, dryRun: boolean): Promise<boolean> {
  const fileConfig = config.files[fileName];
  const exists = await sheetExists(fileName);

  if (!exists) {
    console.log(`  ⚠ Sheet "${fileName}" not found, skipping`);
    return false;
  }

  const rows = await readSheet(fileName);
  if (rows.length < 2) {
    console.log(`  ⚠ Sheet "${fileName}" is empty, skipping`);
    return false;
  }

  const original = await readJsonFile(fileName);
  let updates: JsonObject;

  if (fileConfig.type === 'array' && fileConfig.arrayPath) {
    const arrayData = parseArraySheet(rows);
    updates = structuredClone(original);
    setNestedArray(updates, fileConfig.arrayPath, arrayData);
  }
  else {
    updates = parseKeyValueSheet(rows);
  }

  const { merged, changes } = mergeWithBlacklist(original, updates, fileName);
  const visibleChanges = changes.filter(c => c.oldValue !== c.newValue);

  if (visibleChanges.length === 0) {
    console.log(`  ✓ ${fileName}: No changes`);
    return false;
  }

  console.log(`  ${fileName}: ${visibleChanges.length} change(s)`);
  for (const change of visibleChanges.slice(0, 5)) {
    console.log(formatChange(change.path, change.oldValue, change.newValue));
  }
  if (visibleChanges.length > 5) {
    console.log(`    ... and ${visibleChanges.length - 5} more`);
  }

  if (!dryRun) {
    await writeJsonFile(fileName, merged);
    console.log(`  ✓ Written to ${config.dataDir}/${fileName}.json`);
  }

  return true;
}

async function pushFile(fileName: FileName): Promise<void> {
  const fileConfig = config.files[fileName];
  const json = await readJsonFile(fileName);

  let rows: string[][];

  if (fileConfig.type === 'array' && fileConfig.arrayPath) {
    const arrayData = getNestedValue(json, fileConfig.arrayPath) as JsonArray;
    rows = exportToArraySheet(arrayData, fileName, fileConfig.arrayPath);
  }
  else {
    rows = exportToKeyValue(json, fileName);
  }

  const exists = await sheetExists(fileName);
  if (!exists) {
    await createSheet(fileName);
    console.log(`  ✓ Created sheet "${fileName}"`);
  }

  await writeSheet(fileName, rows);
  console.log(`  ✓ Pushed ${rows.length - 1} row(s) to "${fileName}"`);
}

function setNestedArray(obj: JsonObject, path: string, value: JsonArray): void {
  const parts = path.split('.');
  let current: JsonObject = obj;

  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    if (current[part] === undefined) {
      current[part] = {};
    }
    current = current[part] as JsonObject;
  }

  current[parts[parts.length - 1]] = value;
}

// CLI Commands

program
  .name('sync-content')
  .description('Sync content between Google Sheets and JSON files')
  .version('1.0.0');

program
  .command('pull')
  .description('Pull content from Google Sheets and update JSON files')
  .option('--dry-run', 'Show changes without writing files')
  .option('-f, --file <name>', 'Sync only specific file')
  .action(async (opts: PullOptions) => {
    validateConfig();
    console.log('\nPulling from Google Sheets...\n');

    const files = opts.file ? [opts.file as FileName] : fileNames;

    if (opts.file && !fileNames.includes(opts.file as FileName)) {
      console.error(`Unknown file: ${opts.file}`);
      console.error(`Available: ${fileNames.join(', ')}`);
      process.exit(1);
    }

    let hasChanges = false;
    for (const fileName of files) {
      const changed = await pullFile(fileName, opts.dryRun ?? false);
      if (changed)
        hasChanges = true;
    }

    if (opts.dryRun) {
      console.log('\n(Dry run - no files written)');
    }
    else if (!hasChanges) {
      console.log('\nAll files up to date');
    }
  });

program
  .command('push')
  .description('Push current JSON content to Google Sheets (initial setup)')
  .option('-f, --file <name>', 'Push only specific file')
  .action(async (opts: PushOptions) => {
    validateConfig();
    console.log('\nPushing to Google Sheets...\n');

    const files = opts.file ? [opts.file as FileName] : fileNames;

    if (opts.file && !fileNames.includes(opts.file as FileName)) {
      console.error(`Unknown file: ${opts.file}`);
      console.error(`Available: ${fileNames.join(', ')}`);
      process.exit(1);
    }

    // Validate all files before pushing any
    let hasErrors = false;
    for (const fileName of files) {
      const json = await readJsonFile(fileName);
      const errors = validateContent(json);
      if (errors.length > 0) {
        hasErrors = true;
        console.log(`  ✗ ${fileName}: ${errors.length} validation error(s)`);
        for (const err of errors) {
          console.log(`    ${err.path}: ${err.reason}`);
          console.log(`      got: ${err.value.length > 80 ? `${err.value.slice(0, 80)}...` : err.value}`);
        }
      }
    }

    if (hasErrors) {
      console.log('\nPush aborted due to validation errors. Fix the issues above and retry.');
      process.exit(1);
    }

    for (const fileName of files) {
      await pushFile(fileName);
    }

    console.log('\nDone!');
  });

program
  .command('diff')
  .description('Show differences between Sheet and local JSON')
  .option('-f, --file <name>', 'Diff only specific file')
  .action(async (opts: { file?: string }) => {
    validateConfig();
    console.log('\nComparing Sheet with local JSON...\n');

    const files = opts.file ? [opts.file as FileName] : fileNames;

    for (const fileName of files) {
      const fileConfig = config.files[fileName];
      const exists = await sheetExists(fileName);

      if (!exists) {
        console.log(`${fileName}: Sheet not found`);
        continue;
      }

      const rows = await readSheet(fileName);
      if (rows.length < 2) {
        console.log(`${fileName}: Sheet empty`);
        continue;
      }

      const original = await readJsonFile(fileName);
      let updates: JsonObject;

      if (fileConfig.type === 'array' && fileConfig.arrayPath) {
        const arrayData = parseArraySheet(rows);
        updates = structuredClone(original);
        setNestedArray(updates, fileConfig.arrayPath, arrayData);
      }
      else {
        updates = parseKeyValueSheet(rows);
      }

      const changes = diffObjects(original, updates, fileName);

      if (changes.length === 0) {
        console.log(`${fileName}: No differences`);
      }
      else {
        console.log(`${fileName}: ${changes.length} difference(s)`);
        for (const change of changes) {
          console.log(formatChange(change.path, change.oldValue, change.newValue));
        }
      }
      console.log('');
    }
  });

program
  .command('blacklist')
  .description('Show blacklisted paths for a file')
  .argument('[file]', 'File name (shows all if omitted)')
  .action((file?: string) => {
    const files = file ? [file as FileName] : fileNames;

    for (const fileName of files) {
      const patterns = getBlacklistPatterns(fileName);
      console.log(`\n${fileName}:`);
      if (patterns.length === 0) {
        console.log('  (no blacklisted paths)');
      }
      else {
        for (const pattern of patterns) {
          console.log(`  - ${pattern}`);
        }
      }
    }
  });

program.parse();
