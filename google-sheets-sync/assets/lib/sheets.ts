import type { SheetData } from './types';
import { google } from 'googleapis';
import { config } from '../config';

async function getAuthClient() {
  const auth = new google.auth.GoogleAuth({
    keyFile: config.credentialsPath,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });
  return auth.getClient();
}

export async function readSheet(sheetName: string): Promise<SheetData> {
  const auth = await getAuthClient();
  const sheets = google.sheets({ version: 'v4', auth });

  const response = await sheets.spreadsheets.values.get({
    spreadsheetId: config.spreadsheetId,
    range: `${sheetName}!A:ZZ`,
  });

  return (response.data.values as SheetData) || [];
}

export async function writeSheet(sheetName: string, values: SheetData): Promise<void> {
  const auth = await getAuthClient();
  const sheets = google.sheets({ version: 'v4', auth });

  // Clear existing content first
  await sheets.spreadsheets.values.clear({
    spreadsheetId: config.spreadsheetId,
    range: `${sheetName}!A:ZZ`,
  });

  // Write new values
  await sheets.spreadsheets.values.update({
    spreadsheetId: config.spreadsheetId,
    range: `${sheetName}!A1`,
    valueInputOption: 'RAW',
    requestBody: { values },
  });
}

export async function sheetExists(sheetName: string): Promise<boolean> {
  const auth = await getAuthClient();
  const sheets = google.sheets({ version: 'v4', auth });

  const response = await sheets.spreadsheets.get({
    spreadsheetId: config.spreadsheetId,
  });

  const sheetNames = response.data.sheets?.map(s => s.properties?.title) || [];
  return sheetNames.includes(sheetName);
}

export async function createSheet(sheetName: string): Promise<void> {
  const auth = await getAuthClient();
  const sheets = google.sheets({ version: 'v4', auth });

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId: config.spreadsheetId,
    requestBody: {
      requests: [{ addSheet: { properties: { title: sheetName } } }],
    },
  });
}
