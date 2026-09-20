import type { JsonObject } from './types';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { config } from '../config';

const projectRoot = join(import.meta.dir, '../../..');

export async function readJsonFile(fileName: string): Promise<JsonObject> {
  const filePath = join(projectRoot, config.dataDir, `${fileName}.json`);
  const content = await readFile(filePath, 'utf-8');
  return JSON.parse(content);
}

export async function writeJsonFile(fileName: string, data: JsonObject): Promise<void> {
  const filePath = join(projectRoot, config.dataDir, `${fileName}.json`);
  const content = `${JSON.stringify(data, null, 2)}\n`;
  await writeFile(filePath, content, 'utf-8');
}

export function formatChange(path: string, oldVal: unknown, newVal: unknown): string {
  const oldStr = truncate(JSON.stringify(oldVal), 40);
  const newStr = truncate(JSON.stringify(newVal), 40);
  return `  ${path}: ${oldStr} → ${newStr}`;
}

function truncate(str: string | undefined, len: number): string {
  if (str === undefined)
    return 'undefined';
  if (str.length <= len)
    return str;
  return `${str.slice(0, len - 3)}...`;
}
