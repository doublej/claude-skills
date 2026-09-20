export const blacklistConfig: Record<string, string[]> = {
  // Global patterns (apply to all files)
  '*': [
    '**.id',        // hide all id fields
    'metaData',     // hide metadata objects
  ],

  // File-specific blacklists
  // 'products': [
  //   'data.items[*].sku',
  //   'data.items[*].internalCode',
  // ],
};
