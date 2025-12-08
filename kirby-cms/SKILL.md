---
name: kirby-cms
description: Build and customize Kirby CMS websites - flat-file CMS with Panel admin, blueprints, templates, and headless capabilities. Use when creating Kirby sites, configuring blueprints, writing templates/snippets, or integrating the REST API.
---

# Kirby CMS Skill

File-based CMS with a powerful Panel admin interface. No database required.

## When to Use

- Creating Kirby CMS websites or themes
- Configuring Panel blueprints for content structure
- Writing templates, snippets, or controllers
- Building headless/API-driven applications
- Extending Kirby with plugins

## Core Architecture

```
project/
├── content/           # Flat-file content (folders = pages)
│   ├── site.txt       # Global site data
│   └── home/          # Home page folder
│       └── home.txt   # Page content
├── site/
│   ├── blueprints/    # Panel field definitions (YAML)
│   ├── templates/     # Page rendering (PHP)
│   ├── snippets/      # Reusable template parts
│   ├── controllers/   # Template logic (PHP)
│   ├── models/        # Custom page models
│   ├── plugins/       # Extensions
│   └── config/
│       └── config.php # Site configuration
├── assets/            # CSS, JS, images
└── media/             # Generated thumbnails
```

## Quick Start

### Installation

```bash
# Composer (recommended)
composer create-project getkirby/starterkit mysite

# Or download Starterkit/Plainkit from getkirby.com
```

**Requirements:** PHP 8.2+ | Apache/Nginx/Caddy

### Basic Template

```php
<!-- site/templates/default.php -->
<?php snippet('header') ?>

<main>
  <h1><?= $page->title() ?></h1>
  <?= $page->text()->kirbytext() ?>
</main>

<?php snippet('footer') ?>
```

### Basic Blueprint

```yaml
# site/blueprints/pages/default.yml
title: Default Page

fields:
  text:
    type: textarea
    label: Content
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Page** | Folder in `/content/` with a `.txt` file |
| **Blueprint** | YAML file defining Panel fields |
| **Template** | PHP file rendering a page type |
| **Snippet** | Reusable PHP template fragment |
| **Controller** | Logic layer for templates |
| **Field** | Content unit (text, files, pages, etc.) |
| **KirbyText** | Extended Markdown with tags |

## Essential Objects

```php
$kirby   // App instance
$site    // Site object (global data)
$page    // Current page
$pages   // Page collection

// Navigation
$page->children()     // Child pages
$page->parent()       // Parent page
$page->siblings()     // Same-level pages

// Content
$page->title()        // Page title
$page->text()         // Field access
$page->files()        // Attached files
$page->images()       // Image files only
```

## Common Helpers

```php
// URLs & Assets
url('path')           // Full URL
css('assets/main.css')
js('assets/app.js')

// Templates
snippet('header', ['data' => $value])
image('photo.jpg')

// Text processing
$field->kirbytext()   // Parse KirbyText/Markdown
$field->escape()      // HTML escape
$field->toPages()     // Convert to page collection

// Translation
t('key')              // Translate string
```

## Reference Files

For deeper documentation:

- **[Templates & Blueprints](references/templates-blueprints.md)** - Field types, sections, layouts, collections
- **[Panel Field Reference](references/panel-fields.md)** - All 35 field types with examples
- **[API & Plugins](references/api-plugins.md)** - REST API, hooks, plugin development

## Configuration

```php
// site/config/config.php
return [
    'debug' => true,
    'panel' => [
        'install' => true
    ],
    'thumbs' => [
        'quality' => 80
    ],
    'languages' => true,
    'cache' => [
        'pages' => ['active' => true]
    ]
];
```

## Useful Links

- [Kirby Reference](https://getkirby.com/docs/reference) - Complete API reference
- [Kirby Cookbook](https://getkirby.com/docs/cookbook) - Solutions & recipes
- [Kirby Plugins](https://getkirby.com/plugins) - Community extensions
