# Offline Catalog SQL Analytics

The `.lrcat` file is a SQLite 3 database. Read-only queries don't need Lightroom running, the plugin started, or the MCP configured — useful for one-off analytics, dedupe scans, finding orphans, or feeding catalog data to other tools.

**Reference**: [fdenivac/Lightroom-SQL-tools](https://github.com/fdenivac/Lightroom-SQL-tools) (41⭐) — Python wrapper around common queries.

## Critical rules

<safety>
1. **Lightroom must be closed** when querying. Lightroom holds an exclusive lock; an open `.lrcat` will return `database is locked` or, worse, partially-written state.
2. **Read-only by default**. Open with `sqlite3 -readonly`. Direct writes can corrupt the catalog beyond Lightroom's repair tools.
3. **Always work on a backup**. Lightroom's auto-backups live next to the catalog as `<name> Backups/<timestamp>/<name>.lrcat`. Copy one before any experiment.
4. **Catalog format may change between Lightroom Classic major versions**. Schema names below are stable through LR Classic 12.x; verify on your version with `.schema` before scripting.
</safety>

## Locating the catalog

```
macOS: ~/Pictures/Lightroom/<Name>.lrcat
Windows: %USERPROFILE%\Pictures\Lightroom\<Name>.lrcat
```

Open via:
```bash
sqlite3 -readonly "/path/to/Catalog.lrcat"
```

## Schema map (key tables)

```
Adobe_images               — one row per virtual copy/master image
AgLibraryFile              — one row per file on disk (an image points to a file)
AgLibraryFolder            — folder hierarchy
AgLibraryRootFolder        — top-level volume mounts
AgLibraryKeyword           — keyword tree
AgLibraryKeywordImage      — many-to-many: image ↔ keyword
AgLibraryCollection        — collections + collection sets
AgLibraryCollectionImage   — many-to-many: image ↔ collection
AgHarvestedExifMetadata    — denormalized EXIF (camera, lens, ISO, shutter, ...)
AgHarvestedIptcMetadata    — denormalized IPTC (caption, copyright, ...)
Adobe_imageDevelopSettings — develop settings text blob (XMP-like) per image
AgLibraryImport            — import sessions
AgLibraryImportImage       — many-to-many: import ↔ image
```

Joins follow `id_local` (every row has one).

## Common queries

### Photo count by year
```sql
SELECT strftime('%Y', datetime(captureTime)) AS year, COUNT(*) AS n
FROM Adobe_images
GROUP BY year
ORDER BY year;
```

### Top 10 lenses
```sql
SELECT lens, COUNT(*) AS n
FROM AgHarvestedExifMetadata
WHERE lens IS NOT NULL
GROUP BY lens
ORDER BY n DESC
LIMIT 10;
```

### 5-star photos with file paths
```sql
SELECT f.baseName || '.' || f.extension AS filename,
       rf.absolutePath || fol.pathFromRoot || f.idx_filename AS fullpath
FROM Adobe_images ai
JOIN AgLibraryFile f       ON ai.rootFile = f.id_local
JOIN AgLibraryFolder fol   ON f.folder = fol.id_local
JOIN AgLibraryRootFolder rf ON fol.rootFolder = rf.id_local
WHERE ai.rating = 5;
```

### Orphan files (image rows with no file on disk)
Open Lightroom and use Library → Find Missing Photos. Doing this in SQL requires re-checking every path against the filesystem — better delegated to fdenivac's `lrt_check_files.py`.

### Keywords with usage count
```sql
SELECT k.name, COUNT(ki.image) AS n
FROM AgLibraryKeyword k
LEFT JOIN AgLibraryKeywordImage ki ON ki.tag = k.id_local
GROUP BY k.id_local
ORDER BY n DESC;
```

### Photos in a specific collection
```sql
SELECT ai.id_local, f.baseName
FROM Adobe_images ai
JOIN AgLibraryCollectionImage ci ON ci.image = ai.id_local
JOIN AgLibraryCollection c       ON ci.collection = c.id_local
JOIN AgLibraryFile f             ON ai.rootFile = f.id_local
WHERE c.name = 'Portfolio 2026';
```

### Develop-applied vs untouched
```sql
SELECT
  CASE
    WHEN hasDevelopAdjustments = 1.0 THEN 'developed'
    ELSE 'untouched'
  END AS state,
  COUNT(*) AS n
FROM Adobe_images
GROUP BY state;
```

## When SQL is faster than the MCP

| Task | SQL | MCP |
|---|---|---|
| Catalog-wide counts (by lens, ISO, year) | seconds | minutes |
| Find duplicates by filename + size | seconds | not supported |
| Bulk export of metadata to CSV | one query | many `get_photo_metadata` calls |
| Keyword usage histogram | one query | not supported |
| **Apply develop settings** | corrupts catalog | use MCP |
| **Rate / keyword / collection writes** | corrupts catalog | use MCP |

Rule of thumb: read-only catalog statistics → SQL. Any write that touches develop, ratings, keywords, collections, or imports → MCP only (so Lightroom's internal indices stay consistent).

## Using the fdenivac wrapper

```bash
git clone https://github.com/fdenivac/Lightroom-SQL-tools
cd Lightroom-SQL-tools
python3 lrt_query.py --catalog ~/Pictures/Lightroom/Catalog.lrcat \
  "SELECT COUNT(*) FROM Adobe_images"
```

Bundled scripts include `lrt_check_files.py` (orphan detection), `lrt_export_csv.py` (metadata dump), and `lrt_keywords.py` (keyword tree audit). Read its README for the current set.

## Schema introspection

If a query fails, check the actual schema:
```sql
.schema Adobe_images
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
```

Column names occasionally drift (e.g., `developSettingsIDCache` was added in LR Classic 7). Verify before scripting against an unfamiliar version.
