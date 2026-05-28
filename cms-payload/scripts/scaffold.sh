#!/usr/bin/env bash
# Scaffold a Payload CMS 3.0 project
# Usage: scaffold.sh <project-name> [--db postgres|mongodb] [--dir <path>]
set -euo pipefail

PROJECT_NAME="${1:?Usage: scaffold.sh <project-name> [--db postgres|mongodb] [--dir <path>]}"
shift

DB="mongodb"
DIR="."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --db) DB="$2"; shift 2 ;;
    --dir) DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

PROJECT_DIR="$DIR/$PROJECT_NAME"

if [[ -d "$PROJECT_DIR" ]]; then
  echo "Error: $PROJECT_DIR already exists"
  exit 1
fi

echo "Scaffolding Payload CMS 3.0 project: $PROJECT_NAME (db: $DB)"

mkdir -p "$PROJECT_DIR/src/collections"
mkdir -p "$PROJECT_DIR/src/globals"
mkdir -p "$PROJECT_DIR/src/hooks"
mkdir -p "$PROJECT_DIR/src/access"
mkdir -p "$PROJECT_DIR/src/app/(payload)/admin/[[...segments]]"
mkdir -p "$PROJECT_DIR/src/app/(payload)/api/[...slug]"
mkdir -p "$PROJECT_DIR/src/app/(frontend)"

# --- .env.example ---
cat > "$PROJECT_DIR/.env.example" << 'ENVEOF'
DATABASE_URL=
PAYLOAD_SECRET=
ENVEOF

# --- .gitignore ---
cat > "$PROJECT_DIR/.gitignore" << 'GIEOF'
node_modules/
.next/
*.tsbuildinfo
.env
dist/
payload-types.ts
GIEOF

# --- tsconfig.json ---
cat > "$PROJECT_DIR/tsconfig.json" << 'TSEOF'
{
  "compilerOptions": {
    "baseUrl": ".",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"],
      "@payload-config": ["./src/payload.config.ts"]
    },
    "target": "ES2022"
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
TSEOF

# --- next.config.ts ---
cat > "$PROJECT_DIR/next.config.ts" << 'NCEOF'
import { withPayload } from '@payloadcms/next/withPayload'
import type { NextConfig } from 'next'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(__filename)

const nextConfig: NextConfig = {
  images: {
    localPatterns: [{ pathname: '/api/media/file/**' }],
  },
  webpack: (webpackConfig) => {
    webpackConfig.resolve.extensionAlias = {
      '.cjs': ['.cts', '.cjs'],
      '.js': ['.ts', '.tsx', '.js', '.jsx'],
      '.mjs': ['.mts', '.mjs'],
    }
    return webpackConfig
  },
  turbopack: {
    root: path.resolve(dirname),
  },
}

export default withPayload(nextConfig, { devBundleServerPackages: false })
NCEOF

# --- DB-specific config ---
if [[ "$DB" == "postgres" ]]; then
  DB_IMPORT="import { postgresAdapter } from '@payloadcms/db-postgres'"
  DB_CONFIG="db: postgresAdapter({
    pool: {
      connectionString: process.env.DATABASE_URL || '',
    },
  }),"
  DB_PKG="@payloadcms/db-postgres"
else
  DB_IMPORT="import { mongooseAdapter } from '@payloadcms/db-mongodb'"
  DB_CONFIG="db: mongooseAdapter({
    url: process.env.DATABASE_URL || '',
  }),"
  DB_PKG="@payloadcms/db-mongodb"
fi

# --- payload.config.ts ---
cat > "$PROJECT_DIR/src/payload.config.ts" << PCEOF
${DB_IMPORT}
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import path from 'path'
import { buildConfig } from 'payload'
import { fileURLToPath } from 'url'
import sharp from 'sharp'

import { Users } from './collections/Users'
import { Media } from './collections/Media'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

export default buildConfig({
  admin: {
    user: Users.slug,
    importMap: {
      baseDir: path.resolve(dirname),
    },
  },
  collections: [Users, Media],
  editor: lexicalEditor(),
  secret: process.env.PAYLOAD_SECRET || '',
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  ${DB_CONFIG}
  sharp,
  plugins: [],
})
PCEOF

# --- Collections ---
cat > "$PROJECT_DIR/src/collections/Users.ts" << 'CEOF'
import type { CollectionConfig } from 'payload'

export const Users: CollectionConfig = {
  slug: 'users',
  admin: {
    useAsTitle: 'email',
  },
  auth: true,
  fields: [],
}
CEOF

cat > "$PROJECT_DIR/src/collections/Media.ts" << 'CEOF'
import type { CollectionConfig } from 'payload'

export const Media: CollectionConfig = {
  slug: 'media',
  access: {
    read: () => true,
  },
  fields: [
    {
      name: 'alt',
      type: 'text',
      required: true,
    },
  ],
  upload: true,
}
CEOF

# --- App routes (payload admin) ---
cat > "$PROJECT_DIR/src/app/(payload)/admin/[[...segments]]/page.tsx" << 'AEOF'
/* THIS FILE WAS GENERATED AUTOMATICALLY BY PAYLOAD. */
/* DO NOT MODIFY IT BECAUSE IT COULD BE REWRITTEN AT ANY TIME. */
import type { Metadata } from 'next'

import config from '@payload-config'
import { RootPage, generatePageMetadata } from '@payloadcms/next/views'
import { importMap } from '../importMap.js'

type Args = {
  params: Promise<{ segments: string[] }>
  searchParams: Promise<{ [key: string]: string | string[] }>
}

export const generateMetadata = ({ params, searchParams }: Args): Promise<Metadata> =>
  generatePageMetadata({ config, params, searchParams })

const Page = ({ params, searchParams }: Args) =>
  RootPage({ config, importMap, params, searchParams })

export default Page
AEOF

cat > "$PROJECT_DIR/src/app/(payload)/api/[...slug]/route.ts" << 'REOF'
/* THIS FILE WAS GENERATED AUTOMATICALLY BY PAYLOAD. */
/* DO NOT MODIFY IT BECAUSE IT COULD BE REWRITTEN AT ANY TIME. */
import config from '@payload-config'
import '@payloadcms/next/css'
import { REST_DELETE, REST_GET, REST_OPTIONS, REST_PATCH, REST_POST, REST_PUT } from '@payloadcms/next/routes'

export const GET = REST_GET(config)
export const POST = REST_POST(config)
export const DELETE = REST_DELETE(config)
export const PATCH = REST_PATCH(config)
export const PUT = REST_PUT(config)
export const OPTIONS = REST_OPTIONS(config)
REOF

cat > "$PROJECT_DIR/src/app/(payload)/layout.tsx" << 'LEOF'
/* THIS FILE WAS GENERATED AUTOMATICALLY BY PAYLOAD. */
import config from '@payload-config'
import '@payloadcms/next/css'
import type { ServerFunctionClient } from 'payload'
import { handleServerFunctions, RootLayout } from '@payloadcms/next/layouts'
import React from 'react'

import { importMap } from './admin/importMap.js'

type Args = {
  children: React.ReactNode
}

const serverFunction: ServerFunctionClient = async function (args) {
  'use server'
  return handleServerFunctions({
    ...args,
    config,
    importMap,
  })
}

const Layout = ({ children }: Args) => (
  <RootLayout config={config} importMap={importMap} serverFunction={serverFunction}>
    {children}
  </RootLayout>
)

export default Layout
LEOF

cat > "$PROJECT_DIR/src/app/(payload)/custom.scss" << 'SEOF'
// Add custom admin styles here
SEOF

# --- Frontend ---
cat > "$PROJECT_DIR/src/app/(frontend)/layout.tsx" << 'FLEOF'
import React from 'react'

export default function FrontendLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
FLEOF

cat > "$PROJECT_DIR/src/app/(frontend)/page.tsx" << 'FPEOF'
import React from 'react'

export default function HomePage() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  )
}
FPEOF

# --- package.json ---
cat > "$PROJECT_DIR/package.json" << PEOF
{
  "name": "${PROJECT_NAME}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "cross-env NODE_OPTIONS=--no-deprecation next dev",
    "build": "cross-env NODE_OPTIONS=\"--no-deprecation --max-old-space-size=8000\" next build",
    "start": "cross-env NODE_OPTIONS=--no-deprecation next start",
    "generate:types": "cross-env NODE_OPTIONS=--no-deprecation payload generate:types",
    "generate:importmap": "cross-env NODE_OPTIONS=--no-deprecation payload generate:importmap",
    "payload": "cross-env NODE_OPTIONS=--no-deprecation payload",
    "lint": "cross-env NODE_OPTIONS=--no-deprecation eslint ."
  },
  "dependencies": {
    "${DB_PKG}": "latest",
    "@payloadcms/next": "latest",
    "@payloadcms/richtext-lexical": "latest",
    "@payloadcms/ui": "latest",
    "cross-env": "^7.0.3",
    "graphql": "^16.8.1",
    "next": "^16.0.0",
    "payload": "latest",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "sharp": "^0.34.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^16.0.0",
    "typescript": "^5.7.0"
  },
  "engines": {
    "node": "^18.20.2 || >=20.9.0"
  }
}
PEOF

echo ""
echo "Project scaffolded at: $PROJECT_DIR"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_DIR"
echo "  cp .env.example .env  # then fill in DATABASE_URL and PAYLOAD_SECRET"
echo "  pnpm install"
echo "  pnpm dev"
