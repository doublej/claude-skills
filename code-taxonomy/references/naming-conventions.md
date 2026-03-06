# Naming Conventions Reference

Per-language canonical naming conventions for all symbol categories.

## Convention Styles

| Style | Pattern | Example |
|-------|---------|---------|
| `snake_case` | `lower_with_underscores` | `get_user_name` |
| `camelCase` | `lowerThenCapitalized` | `getUserName` |
| `PascalCase` | `AllCapitalized` | `GetUserName` |
| `SCREAMING_SNAKE` | `UPPER_WITH_UNDERSCORES` | `MAX_RETRIES` |
| `kebab-case` | `lower-with-dashes` | `user-profile` |
| `flat` | `alllowercase` | `getuser` |

## Python (PEP 8)

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions | `snake_case` | `calculate_total`, `get_user` |
| Methods | `snake_case` | `process_data`, `_internal_method` |
| Classes | `PascalCase` | `UserProfile`, `HttpClient` |
| Constants | `SCREAMING_SNAKE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Variables | `snake_case` | `user_count`, `is_valid` |
| Modules | `snake_case` | `user_utils.py`, `data_loader.py` |
| Packages | `flat` or `snake_case` | `mypackage`, `my_package` |
| Type aliases | `PascalCase` | `UserId`, `ResponseMap` |

**Private convention:** prefix with `_` for internal, `__` for name-mangled.

## TypeScript / JavaScript

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions | `camelCase` | `calculateTotal`, `getUser` |
| Classes | `PascalCase` | `UserProfile`, `HttpClient` |
| Interfaces | `PascalCase` | `UserData`, `ApiResponse` |
| Types | `PascalCase` | `UserId`, `Config` |
| Enums | `PascalCase` | `Direction`, `Status` |
| Enum members | `PascalCase` | `Direction.North` |
| Constants | `SCREAMING_SNAKE` or `camelCase` | `MAX_RETRIES` or `maxRetries` |
| Variables | `camelCase` | `userCount`, `isValid` |
| Files | `kebab-case` or `PascalCase` | `user-profile.ts` or `UserProfile.tsx` |

**React files:** Component files use `PascalCase` (`UserCard.tsx`). Hooks, utils, and configs use `camelCase` or `kebab-case`.

## Go

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions (exported) | `PascalCase` | `GetUser`, `ParseConfig` |
| Functions (unexported) | `camelCase` | `getUser`, `parseConfig` |
| Types | `PascalCase` | `UserProfile`, `HttpClient` |
| Constants | `PascalCase` or `camelCase` | `MaxRetries`, `defaultTimeout` |
| Variables | `camelCase` | `userCount`, `isValid` |
| Packages | `flat` | `http`, `strconv` |
| Files | `snake_case` | `user_handler.go` |

**Go-specific:** Exported = starts with uppercase. Acronyms stay all-caps: `HTTPClient`, `XMLParser`, `ID`.

## Rust

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions | `snake_case` | `calculate_total`, `get_user` |
| Structs | `PascalCase` | `UserProfile`, `HttpClient` |
| Enums | `PascalCase` | `Direction`, `Status` |
| Enum variants | `PascalCase` | `Direction::North` |
| Traits | `PascalCase` | `Display`, `Iterator` |
| Constants | `SCREAMING_SNAKE` | `MAX_RETRIES`, `DEFAULT_PORT` |
| Statics | `SCREAMING_SNAKE` | `GLOBAL_STATE` |
| Variables | `snake_case` | `user_count`, `is_valid` |
| Modules | `snake_case` | `user_utils`, `data_loader` |
| Files | `snake_case` | `user_handler.rs` |

## Swift

| Category | Convention | Examples |
|----------|-----------|----------|
| Functions | `camelCase` | `calculateTotal()`, `getUser()` |
| Classes | `PascalCase` | `UserProfile`, `NetworkManager` |
| Structs | `PascalCase` | `ContentView`, `UserData` |
| Enums | `PascalCase` | `Direction`, `Status` |
| Enum cases | `camelCase` | `.north`, `.inProgress` |
| Protocols | `PascalCase` | `Codable`, `Identifiable` |
| Constants | `camelCase` | `maxRetries`, `defaultTimeout` |
| Variables | `camelCase` | `userCount`, `isValid` |
| Files | `PascalCase` | `UserProfile.swift` |

**Apple convention:** Protocols often use adjective names (`-able`, `-ible`) or noun names for capability protocols.

## Abbreviation Handling

Common abbreviations that should be preserved as-is in their conventional form:

| Term | In camelCase | In PascalCase | In snake_case |
|------|-------------|---------------|---------------|
| API | `apiKey` | `APIKey` (Go) / `ApiKey` (others) | `api_key` |
| URL | `urlString` | `URLString` (Go) / `UrlString` | `url_string` |
| ID | `userId` | `UserID` (Go) / `UserId` | `user_id` |
| HTTP | `httpClient` | `HTTPClient` (Go) / `HttpClient` | `http_client` |
| JSON | `jsonData` | `JSONData` (Go) / `JsonData` | `json_data` |
| SQL | `sqlQuery` | `SQLQuery` (Go) / `SqlQuery` | `sql_query` |
| XML | `xmlParser` | `XMLParser` (Go) / `XmlParser` | `xml_parser` |
| UI | `uiState` | `UIState` (Go) / `UiState` | `ui_state` |
| IO | `ioStream` | `IOStream` (Go) / `IoStream` | `io_stream` |

**Go exception:** Go keeps acronyms all-caps (`HTTPClient`, `UserID`). All other languages split and capitalize normally (`HttpClient`, `UserId`).

## Framework-Specific Overrides

### React (TS/JS)
- Component files: `PascalCase` (`UserCard.tsx`)
- Hook files: `camelCase` prefixed with `use` (`useAuth.ts`)
- Utility files: `kebab-case` (`format-date.ts`)
- CSS modules: `kebab-case` (`user-card.module.css`)

### Next.js
- Pages/routes: `kebab-case` (`about-us/page.tsx`)
- API routes: `kebab-case` (`api/get-users/route.ts`)

### SvelteKit
- Routes: `kebab-case` (`about-us/+page.svelte`)
- Components: `PascalCase` (`UserCard.svelte`)
- Stores: `camelCase` (`userStore.ts`)

### Django
- Apps: `snake_case` (`user_profiles`)
- Models: `PascalCase` (`UserProfile`)
- Views: `snake_case` (`get_user_list`)

### FastAPI
- Route functions: `snake_case` (`get_users`)
- Models: `PascalCase` (`UserResponse`)
- Settings: `PascalCase` class, `snake_case` fields
