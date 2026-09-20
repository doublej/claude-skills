export type SheetRow = string[];
export type SheetData = SheetRow[];

export type JsonValue = string | number | boolean | null | JsonObject | JsonArray;
export type JsonObject = { [key: string]: JsonValue };
export type JsonArray = JsonValue[];

export type SyncResult = {
  fileName: string;
  hasChanges: boolean;
  changes: FieldChange[];
};

export type FieldChange = {
  path: string;
  oldValue: JsonValue;
  newValue: JsonValue;
};

export type PullOptions = {
  dryRun?: boolean;
  file?: string;
};

export type PushOptions = {
  file?: string;
};
