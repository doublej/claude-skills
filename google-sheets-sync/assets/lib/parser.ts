import type { JsonArray, JsonObject, JsonValue, SheetData } from './types';
import { isBlacklisted } from './path-matcher';

/**
 * Parse a key-value sheet (two columns: path, value)
 */
export function parseKeyValueSheet(rows: SheetData): JsonObject {
  const result: JsonObject = {};

  for (const row of rows.slice(1)) {
    const [keyPath, value] = row;
    if (!keyPath || keyPath.startsWith('#'))
      continue;
    setNestedValue(result, keyPath, parseValue(value));
  }

  return result;
}

/**
 * Parse an array sheet (first row headers, remaining rows are items)
 */
export function parseArraySheet(rows: SheetData): JsonArray {
  if (rows.length < 2)
    return [];

  const headers = rows[0];
  const result: JsonArray = [];

  for (const row of rows.slice(1)) {
    if (!row.some(cell => cell?.trim()))
      continue;
    const item: JsonObject = {};

    headers.forEach((header, i) => {
      const value = row[i];
      if (value !== undefined && value !== '') {
        setNestedValue(item, header, parseValue(value));
      }
    });

    result.push(item);
  }

  return result;
}

/**
 * Export JSON object to key-value format, excluding blacklisted paths
 */
export function exportToKeyValue(obj: JsonObject, fileName: string, prefix = ''): SheetData {
  const rows: SheetData = [['Key Path', 'Value']];
  flattenObject(obj, prefix, rows, fileName);
  return rows;
}

/**
 * Export array to row-based format, excluding blacklisted columns
 */
export function exportToArraySheet(items: JsonArray, fileName: string, arrayPath: string): SheetData {
  if (items.length === 0)
    return [[]];

  const allHeaders = extractHeaders(items[0] as JsonObject);
  // Filter out blacklisted headers (check with full path: arrayPath[*].header)
  const headers = allHeaders.filter((h) => {
    const fullPath = `${arrayPath}[*].${h}`;
    return !isBlacklisted(fullPath, fileName);
  });

  const rows: SheetData = [headers];

  for (const item of items) {
    const row = headers.map((h) => {
      const val = getNestedValue(item as JsonObject, h);
      return val !== undefined ? String(val) : '';
    });
    rows.push(row);
  }

  return rows;
}

function parseValue(value: string | undefined): JsonValue {
  if (value === undefined || value === '')
    return '';
  if (value === 'true')
    return true;
  if (value === 'false')
    return false;
  if (value === 'null')
    return null;
  const num = Number(value);
  if (!Number.isNaN(num) && value.trim() !== '')
    return num;
  return value;
}

function setNestedValue(obj: JsonObject, path: string, value: JsonValue): void {
  const parts = parsePath(path);
  let current: JsonValue = obj;

  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    const nextPart = parts[i + 1];
    const isNextArray = typeof nextPart === 'number';

    if (typeof part === 'number') {
      const arr = current as JsonArray;
      if (arr[part] === undefined) {
        arr[part] = isNextArray ? [] : {};
      }
      current = arr[part];
    }
    else {
      const o = current as JsonObject;
      if (o[part] === undefined) {
        o[part] = isNextArray ? [] : {};
      }
      current = o[part];
    }
  }

  const lastPart = parts[parts.length - 1];
  if (typeof lastPart === 'number') {
    (current as JsonArray)[lastPart] = value;
  }
  else {
    (current as JsonObject)[lastPart] = value;
  }
}

export function getNestedValue(obj: JsonObject, path: string): JsonValue {
  const parts = parsePath(path);
  let current: JsonValue = obj;

  for (const part of parts) {
    if (current === null || current === undefined)
      return undefined as unknown as JsonValue;
    if (typeof part === 'number') {
      current = (current as JsonArray)[part];
    }
    else {
      current = (current as JsonObject)[part];
    }
  }

  return current;
}

function parsePath(path: string): (string | number)[] {
  const parts: (string | number)[] = [];
  const regex = /([^.[\]]+)|\[(\d+)\]/g;

  for (const match of path.matchAll(regex)) {
    if (match[1] !== undefined) {
      parts.push(match[1]);
    }
    else if (match[2] !== undefined) {
      parts.push(Number.parseInt(match[2], 10));
    }
  }

  return parts;
}

function flattenObject(obj: JsonValue, prefix: string, rows: SheetData, fileName: string): void {
  // Skip blacklisted paths
  if (prefix && isBlacklisted(prefix, fileName)) {
    return;
  }

  if (obj === null || typeof obj !== 'object') {
    rows.push([prefix, String(obj ?? '')]);
    return;
  }

  if (Array.isArray(obj)) {
    obj.forEach((item, i) => {
      flattenObject(item, `${prefix}[${i}]`, rows, fileName);
    });
    return;
  }

  for (const [key, value] of Object.entries(obj)) {
    const newPrefix = prefix ? `${prefix}.${key}` : key;
    flattenObject(value, newPrefix, rows, fileName);
  }
}

function extractHeaders(item: JsonObject, prefix = ''): string[] {
  const headers: string[] = [];

  for (const [key, value] of Object.entries(item)) {
    const path = prefix ? `${prefix}.${key}` : key;

    if (value === null || typeof value !== 'object') {
      headers.push(path);
    }
    else if (Array.isArray(value)) {
      value.forEach((v, i) => {
        if (v !== null && typeof v === 'object' && !Array.isArray(v)) {
          headers.push(...extractHeaders(v as JsonObject, `${path}[${i}]`));
        }
        else {
          headers.push(`${path}[${i}]`);
        }
      });
    }
    else {
      headers.push(...extractHeaders(value as JsonObject, path));
    }
  }

  return headers;
}
