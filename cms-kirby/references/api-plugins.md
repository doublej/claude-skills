# API & Plugin Reference

## REST API

Kirby includes a full REST API for headless usage.

### Authentication

```bash
# Basic Auth (email:password base64 encoded)
curl -u "user@example.com:password" \
  https://example.com/api/pages/blog

# Bearer Token (from Panel)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://example.com/api/pages/blog
```

PHP authentication:

```php
// site/config/config.php
return [
    'api' => [
        'basicAuth' => true,
        'allowInsecure' => false  // Require HTTPS
    ]
];
```

### API Endpoints

```
GET    /api/site                    # Site data
GET    /api/pages/:id               # Single page
GET    /api/pages/:id/children      # Page children
GET    /api/pages/:id/files         # Page files
GET    /api/pages/:id/files/:filename

GET    /api/users                   # All users
GET    /api/users/:id               # Single user
GET    /api/roles                   # Available roles
GET    /api/languages               # Languages (if multi-lang)
GET    /api/translations            # Panel translations
```

### API Response

```json
{
  "code": 200,
  "data": {
    "id": "blog/article",
    "slug": "article",
    "url": "https://example.com/blog/article",
    "title": "My Article",
    "content": {
      "text": "Article content...",
      "date": "2024-01-15"
    },
    "files": [...],
    "children": [...]
  },
  "status": "ok"
}
```

### Custom API Routes

```php
// site/config/config.php
return [
    'api' => [
        'routes' => [
            [
                'pattern' => 'search',
                'action'  => function () {
                    $query = get('q');
                    $results = site()->search($query, 'title|text');

                    return $results->map(fn($page) => [
                        'title' => $page->title()->value(),
                        'url'   => $page->url()
                    ])->values();
                }
            ]
        ]
    ]
];
```

---

## Routes

Define custom URL routes:

```php
// site/config/config.php
return [
    'routes' => [
        // Simple redirect
        [
            'pattern' => 'old-page',
            'action'  => fn() => go('new-page')
        ],

        // Dynamic route
        [
            'pattern' => 'products/(:any)',
            'action'  => function ($slug) {
                $product = page('shop')->children()->findBy('slug', $slug);
                if (!$product) {
                    return site()->errorPage();
                }
                return $product;
            }
        ],

        // Before routes (authentication)
        [
            'pattern' => 'dashboard/(:all)',
            'action'  => function ($path) {
                if (!kirby()->user()) {
                    go('login');
                }
                return $this->next();
            }
        ],

        // JSON response
        [
            'pattern' => 'api/posts.json',
            'action'  => function () {
                $posts = page('blog')->children()->listed();
                return Response::json($posts->toArray());
            }
        ]
    ]
];
```

### Route Patterns

```php
'(:any)'    // Any single segment: blog/(:any) → blog/my-post
'(:all)'    // All remaining segments: files/(:all) → files/path/to/file
'(:num)'    // Numbers only: page/(:num) → page/42
'(:alpha)'  // Letters only: user/(:alpha) → user/john
'(:alphanum)' // Alphanumeric
```

---

## Hooks

Execute code on events:

```php
// site/config/config.php
return [
    'hooks' => [
        // Page hooks
        'page.create:after' => function ($page) {
            // Send notification
        },
        'page.update:after' => function ($newPage, $oldPage) {
            // Log changes
        },
        'page.delete:before' => function ($page) {
            // Prevent deletion
            if ($page->children()->count() > 0) {
                throw new Exception('Cannot delete pages with children');
            }
        },
        'page.changeStatus:after' => function ($newPage, $oldPage) {
            // Notify on publish
            if ($newPage->isListed() && !$oldPage->isListed()) {
                // Send publish notification
            }
        },

        // File hooks
        'file.create:after' => function ($file) {
            // Process uploaded file
        },

        // User hooks
        'user.login:after' => function ($user) {
            // Log login
        },

        // Route hooks
        'route:before' => function ($route, $path, $method) {
            // Global middleware
        },

        // System hooks
        'system.exception' => function ($exception) {
            // Error logging
        }
    ]
];
```

### Available Hooks

```
page.create:before/after
page.update:before/after
page.delete:before/after
page.changeSlug:before/after
page.changeStatus:before/after
page.changeTitle:before/after
page.changeTemplate:before/after
page.duplicate:after

file.create:before/after
file.update:before/after
file.delete:before/after
file.replace:before/after

user.create:before/after
user.update:before/after
user.delete:before/after
user.login:before/after
user.logout:before/after
user.changeEmail:before/after
user.changePassword:before/after
user.changeRole:before/after

site.update:before/after

route:before/after
system.loadPlugins:after
system.exception
```

---

## Plugins

### Plugin Structure

```
site/plugins/my-plugin/
├── index.php           # Plugin entry point (required)
├── composer.json       # Package info
└── src/
    ├── components/     # Vue components
    └── ...
```

### Basic Plugin

```php
<?php
// site/plugins/my-plugin/index.php

Kirby::plugin('yourname/my-plugin', [
    'options' => [
        'enabled' => true
    ]
]);
```

### Plugin Extensions

```php
<?php
Kirby::plugin('yourname/my-plugin', [

    // Custom field types
    'fields' => [
        'myfield' => [
            'props' => [
                'value' => fn($value = null) => $value
            ]
        ]
    ],

    // Custom page methods
    'pageMethods' => [
        'readingTime' => function () {
            return ceil(str_word_count($this->text()->value()) / 200);
        }
    ],

    // Custom file methods
    'fileMethods' => [
        'sizeFormatted' => function () {
            return $this->niceSize();
        }
    ],

    // Custom field methods
    'fieldMethods' => [
        'toUppercase' => function ($field) {
            return strtoupper($field->value);
        }
    ],

    // Custom KirbyTags
    'tags' => [
        'youtube' => [
            'attr' => ['width', 'height'],
            'html' => function ($tag) {
                return '<iframe src="https://youtube.com/embed/' .
                       $tag->value . '"></iframe>';
            }
        ]
    ],

    // API routes
    'api' => [
        'routes' => [
            [
                'pattern' => 'my-endpoint',
                'action'  => fn() => ['status' => 'ok']
            ]
        ]
    ],

    // Routes
    'routes' => [
        [
            'pattern' => 'my-route',
            'action'  => fn() => 'Hello!'
        ]
    ],

    // Hooks
    'hooks' => [
        'page.update:after' => function ($page) {
            // React to page updates
        }
    ],

    // Blueprints
    'blueprints' => [
        'pages/custom' => __DIR__ . '/blueprints/pages/custom.yml'
    ],

    // Templates
    'templates' => [
        'custom' => __DIR__ . '/templates/custom.php'
    ],

    // Snippets
    'snippets' => [
        'my-snippet' => __DIR__ . '/snippets/my-snippet.php'
    ],

    // Controllers
    'controllers' => [
        'custom' => function ($page) {
            return ['data' => 'value'];
        }
    ],

    // Collections
    'collections' => [
        'featured' => function ($site) {
            return $site->children()->listed()->limit(5);
        }
    ],

    // Translations
    'translations' => [
        'en' => [
            'my.translation' => 'English text'
        ],
        'de' => [
            'my.translation' => 'German text'
        ]
    ]
]);
```

### Plugin Options

```php
// Plugin definition
Kirby::plugin('yourname/my-plugin', [
    'options' => [
        'apiKey' => null,
        'enabled' => true
    ]
]);

// Usage in config.php
return [
    'yourname.my-plugin' => [
        'apiKey' => 'secret',
        'enabled' => true
    ]
];

// Access in plugin
option('yourname.my-plugin.apiKey');
```

---

## Components

Override core Kirby components:

```php
Kirby::plugin('yourname/my-plugin', [
    'components' => [
        // Custom Markdown parser
        'markdown' => function ($kirby, string $text, array $options = []): string {
            return MyCustomMarkdown::parse($text);
        },

        // Custom SmartyPants
        'smartypants' => function ($kirby, string $text, array $options = []): string {
            return MyCustomSmartypants::parse($text);
        },

        // Custom thumb generator
        'thumb' => function ($kirby, string $src, string $dst, array $options): string {
            // Custom thumbnail generation
            return $dst;
        }
    ]
]);
```

---

## Headless Setup

Configure Kirby as headless CMS:

```php
// site/config/config.php
return [
    'api' => [
        'basicAuth' => true,
        'allowInsecure' => false
    ],

    // Disable frontend
    'routes' => [
        [
            'pattern' => '(:all)',
            'action'  => function ($path) {
                // Allow Panel access
                if (Str::startsWith($path, 'panel')) {
                    return $this->next();
                }
                // Redirect everything else to API
                return Response::json(['error' => 'Use /api endpoints'], 404);
            }
        ]
    ],

    // CORS for frontend apps
    'api' => [
        'routes' => [
            [
                'pattern' => '(:all)',
                'method'  => 'OPTIONS',
                'action'  => function () {
                    return new Response('', 'text/plain', 200, [
                        'Access-Control-Allow-Origin'  => '*',
                        'Access-Control-Allow-Methods' => 'GET, POST, OPTIONS',
                        'Access-Control-Allow-Headers' => 'Authorization, Content-Type'
                    ]);
                }
            ]
        ]
    ]
];
```

---

## Caching

```php
// site/config/config.php
return [
    'cache' => [
        'pages' => [
            'active' => true,
            'type'   => 'file',
            'prefix' => 'pages',
            'ignore' => function ($page) {
                return $page->template() === 'api';
            }
        ],

        'api' => [
            'active' => true,
            'type'   => 'apcu'
        ]
    ]
];
```

Cache API:

```php
$cache = kirby()->cache('pages');

// Store
$cache->set('key', $data, 60); // 60 minutes

// Retrieve
$data = $cache->get('key');

// Remove
$cache->remove('key');

// Flush all
$cache->flush();
```
