import { blacklistConfig } from '../blacklist.config';

/**
 * Check if a path is blacklisted for a given file
 * Patterns:
 *   - ** matches any nested path segments
 *   - [*] matches any array index
 */
export function isBlacklisted(path: string, fileName: string): boolean {
  const patterns = [
    ...(blacklistConfig['*'] || []),
    ...(blacklistConfig[fileName] || []),
  ];
  return patterns.some(pattern => matchPattern(path, pattern));
}

function matchPattern(path: string, pattern: string): boolean {
  const regexStr = pattern
    .replace(/\./g, '\\.')
    .replace(/\[\*\]/g, '\\[\\d+\\]')
    .replace(/\*\*/g, '.*');

  // Match exact path OR path is nested under pattern (e.g. pattern "foo.bar" matches "foo.bar.baz")
  const exactRegex = new RegExp(`^${regexStr}$`);
  const prefixRegex = new RegExp(`^${regexStr}[.\\[]`);
  return exactRegex.test(path) || prefixRegex.test(path);
}

/**
 * Get all blacklisted paths for a file (for display)
 */
export function getBlacklistPatterns(fileName: string): string[] {
  return [
    ...(blacklistConfig['*'] || []),
    ...(blacklistConfig[fileName] || []),
  ];
}
