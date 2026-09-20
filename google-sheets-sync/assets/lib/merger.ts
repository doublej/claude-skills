import type { FieldChange, JsonArray, JsonObject, JsonValue } from './types';
import { isBlacklisted } from './path-matcher';

export type MergeResult = {
  merged: JsonObject;
  changes: FieldChange[];
};

/**
 * Deep merge updates into original, skipping blacklisted paths
 */
export function mergeWithBlacklist(
  original: JsonObject,
  updates: JsonObject,
  fileName: string,
): MergeResult {
  const changes: FieldChange[] = [];
  const merged = deepMerge(original, updates, '', fileName, changes);
  return { merged: merged as JsonObject, changes };
}

function deepMerge(
  original: JsonValue,
  updates: JsonValue,
  currentPath: string,
  fileName: string,
  changes: FieldChange[],
): JsonValue {
  // If path is blacklisted, keep original
  if (currentPath && isBlacklisted(currentPath, fileName)) {
    return original;
  }

  // Handle arrays
  if (Array.isArray(updates)) {
    if (!Array.isArray(original)) {
      changes.push({ path: currentPath, oldValue: original, newValue: updates });
      return updates;
    }

    const result: JsonArray = [];
    const maxLen = Math.max(original.length, updates.length);

    for (let i = 0; i < maxLen; i++) {
      const itemPath = `${currentPath}[${i}]`;

      if (i >= updates.length) {
        // Item removed in updates - keep if within original
        result.push(original[i]);
      }
      else if (i >= original.length) {
        // New item in updates
        changes.push({ path: itemPath, oldValue: null, newValue: updates[i] });
        result.push(updates[i]);
      }
      else {
        result.push(deepMerge(original[i], updates[i], itemPath, fileName, changes));
      }
    }

    return result;
  }

  // Handle objects
  if (updates !== null && typeof updates === 'object') {
    if (original === null || typeof original !== 'object' || Array.isArray(original)) {
      changes.push({ path: currentPath, oldValue: original, newValue: updates });
      return updates;
    }

    const result: JsonObject = { ...original };

    for (const key of Object.keys(updates)) {
      const newPath = currentPath ? `${currentPath}.${key}` : key;
      result[key] = deepMerge(original[key], (updates as JsonObject)[key], newPath, fileName, changes);
    }

    return result;
  }

  // Primitive values
  if (original !== updates) {
    changes.push({ path: currentPath, oldValue: original, newValue: updates });
  }

  return updates;
}

/**
 * Compare two objects and return differences
 */
export function diffObjects(
  original: JsonObject,
  updates: JsonObject,
  fileName: string,
): FieldChange[] {
  const changes: FieldChange[] = [];
  deepMerge(original, updates, '', fileName, changes);
  return changes.filter(c => !isBlacklisted(c.path, fileName));
}
