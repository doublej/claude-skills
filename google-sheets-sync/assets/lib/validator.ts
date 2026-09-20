import type { JsonObject, JsonValue } from './types';

export type ValidationError = {
  path: string;
  value: string;
  reason: string;
};

// Customize these for your project
const LOCAL_PATH_KEYS = new Set(['image', 'thumbnail', 'poster']);
const HTTPS_URL_RE = /^https:\/\/.+/;

export function validateContent(data: JsonObject): ValidationError[] {
  const errors: ValidationError[] = [];
  walk(data, '', errors);
  return errors;
}

function walk(value: JsonValue, path: string, errors: ValidationError[]): void {
  if (value === null || value === undefined)
    return;

  if (Array.isArray(value)) {
    for (let i = 0; i < value.length; i++) {
      walk(value[i], `${path}[${i}]`, errors);
    }
    return;
  }

  if (typeof value === 'object') {
    for (const [key, child] of Object.entries(value as JsonObject)) {
      if (child === undefined)
        continue;
      const childPath = path ? `${path}.${key}` : key;
      walk(child, childPath, errors);
    }
    return;
  }

  if (typeof value !== 'string' || value === '')
    return;

  const key = path.split('.').pop()?.replace(/\[\d+\]$/, '') ?? '';

  // Add your validation rules here
  if (LOCAL_PATH_KEYS.has(key)) {
    validateLocalPath(value, path, errors);
  }
  else if (key === 'href' || key === 'url') {
    validateHref(value, path, errors);
  }
}

function validateLocalPath(value: string, path: string, errors: ValidationError[]): void {
  if (value.startsWith('/'))
    return;
  errors.push({ path, value, reason: 'must be a local path starting with /' });
}

function validateHref(value: string, path: string, errors: ValidationError[]): void {
  if (HTTPS_URL_RE.test(value) || value.startsWith('/'))
    return;
  errors.push({ path, value, reason: 'must be a valid https:// URL or local path' });
}
