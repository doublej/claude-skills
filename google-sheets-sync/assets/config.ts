export type FileConfig = {
  type: 'keyvalue' | 'array';
  arrayPath?: string;
};

export const config = {
  spreadsheetId: process.env.GOOGLE_SHEETS_ID || '',
  credentialsPath: process.env.GOOGLE_CREDENTIALS_PATH || './google-credentials.json',
  dataDir: 'public/data',

  files: {
    // Key-value example: flat settings file
    'settings': { type: 'keyvalue' },

    // Array example: list of items at a nested path
    // 'products': { type: 'array', arrayPath: 'data.items' },
  } satisfies Record<string, FileConfig>,
} as const;

export type FileName = keyof typeof config.files;
