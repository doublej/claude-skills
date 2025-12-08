# Templates & Blueprints Reference

## Templates

Templates render pages. File name matches content file type:
- `content/projects/project.txt` → `site/templates/project.php`

### Template Structure

```php
<?php
// site/templates/article.php

// Access page data
$title = $page->title();
$text = $page->text()->kirbytext();
$date = $page->date()->toDate('F j, Y');

// Access related content
$author = $page->author()->toUser();
$cover = $page->cover()->toFile();
?>

<?php snippet('header') ?>

<article>
  <?php if($cover): ?>
    <img src="<?= $cover->url() ?>" alt="<?= $cover->alt() ?>">
  <?php endif ?>

  <h1><?= $title ?></h1>
  <time><?= $date ?></time>

  <?= $text ?>
</article>

<?php snippet('footer') ?>
```

### Controllers

Add logic to templates. Same filename in `/site/controllers/`:

```php
<?php
// site/controllers/blog.php
return function ($page, $kirby) {
    $articles = $page->children()
        ->listed()
        ->sortBy('date', 'desc');

    $perPage = 10;
    $articles = $articles->paginate($perPage);
    $pagination = $articles->pagination();

    return compact('articles', 'pagination');
};
```

Template receives variables:

```php
<?php // site/templates/blog.php ?>
<?php foreach($articles as $article): ?>
  <h2><?= $article->title() ?></h2>
<?php endforeach ?>
```

### Snippets

Reusable template parts:

```php
<?php
// site/snippets/card.php
/** @var Kirby\Cms\Page $item */
?>
<article class="card">
  <h3><?= $item->title() ?></h3>
  <p><?= $item->intro()->excerpt(100) ?></p>
  <a href="<?= $item->url() ?>">Read more</a>
</article>
```

Usage:

```php
<?php snippet('card', ['item' => $page]) ?>

<!-- With slots (Kirby 4+) -->
<?php snippet('card', slots: true) ?>
  <?php slot('title') ?>Custom Title<?php endslot() ?>
<?php endsnippet() ?>
```

### Page Models

Extend page objects with custom methods:

```php
<?php
// site/models/article.php
class ArticlePage extends Kirby\Cms\Page
{
    public function readingTime(): int
    {
        $words = str_word_count($this->text()->value());
        return ceil($words / 200);
    }
}
```

Usage in template:

```php
<span><?= $page->readingTime() ?> min read</span>
```

---

## Blueprints

YAML files defining Panel structure. Location: `/site/blueprints/`

### Blueprint Types

```
site/blueprints/
├── site.yml           # Site-wide settings
├── pages/
│   ├── default.yml    # Default page type
│   └── article.yml    # Article pages
├── files/
│   ├── image.yml      # Image metadata
│   └── document.yml   # Document metadata
└── users/
    └── editor.yml     # User role
```

### Basic Page Blueprint

```yaml
# site/blueprints/pages/article.yml
title: Article

# Page settings
status:
  draft:
    label: Draft
    text: Not published
  listed:
    label: Published
    text: Publicly visible

# Options
options:
  changeSlug: true
  changeStatus: true
  changeTemplate: false
  delete: true

# Fields
fields:
  intro:
    type: textarea
    label: Introduction
    maxlength: 200

  text:
    type: blocks
    label: Content

  date:
    type: date
    label: Publish Date
    default: today

  author:
    type: users
    label: Author
    max: 1
```

### Sections & Layout

Organize fields into columns and sections:

```yaml
title: Project

columns:
  - width: 2/3
    sections:
      content:
        type: fields
        fields:
          title:
            type: text
          description:
            type: textarea
          gallery:
            type: files
            layout: cards

  - width: 1/3
    sections:
      meta:
        type: fields
        fields:
          date:
            type: date
          status:
            type: select
            options:
              - active
              - completed
              - archived

      files:
        type: files
        headline: Attachments
```

### Field Groups

Reusable field configurations:

```yaml
# site/blueprints/fields/seo.yml
type: group
fields:
  metaTitle:
    type: text
    label: Meta Title
  metaDescription:
    type: textarea
    label: Meta Description
    maxlength: 160
```

Usage:

```yaml
fields:
  seo: fields/seo
```

### Conditional Fields

Show/hide based on other values:

```yaml
fields:
  type:
    type: select
    options:
      - video
      - image

  videoUrl:
    type: url
    label: Video URL
    when:
      type: video

  image:
    type: files
    max: 1
    when:
      type: image
```

### Tabs

Organize large blueprints:

```yaml
title: Complex Page

tabs:
  content:
    label: Content
    icon: text
    columns:
      - width: 1/1
        fields:
          text:
            type: blocks

  media:
    label: Media
    icon: image
    sections:
      gallery:
        type: files

  seo:
    label: SEO
    icon: search
    fields:
      metaTitle:
        type: text
      metaDescription:
        type: textarea
```

---

## Collections

Define reusable page/file collections:

```php
<?php
// site/collections/featured.php
return function ($site) {
    return $site->find('blog')
        ->children()
        ->listed()
        ->filterBy('featured', true)
        ->sortBy('date', 'desc')
        ->limit(3);
};
```

Usage:

```php
<?php foreach(collection('featured') as $article): ?>
  <?php snippet('card', ['item' => $article]) ?>
<?php endforeach ?>
```

---

## Content Representations

Output different formats (JSON, RSS, etc.):

```php
<?php
// site/templates/article.json.php
header('Content-type: application/json');

echo json_encode([
    'title' => $page->title()->value(),
    'text'  => $page->text()->kirbytext()->value(),
    'url'   => $page->url()
]);
```

Access via: `/blog/article.json`

---

## Query Language

Use in blueprints for dynamic content:

```yaml
fields:
  relatedPosts:
    type: pages
    query: site.find('blog').children.listed.limit(10)

  featuredImage:
    type: files
    query: page.images.template('cover')

info:
  type: info
  text: "{{ page.children.count }} child pages"
```

### Query Syntax

```yaml
# Access objects
site                    # Site object
page                    # Current page
kirby.user              # Logged-in user

# Traverse
page.parent             # Parent page
page.children           # Child pages
site.find('blog')       # Find by path

# Filter & sort
page.children.listed    # Only published
page.files.images       # Only images
page.children.sortBy('date', 'desc')
page.children.filterBy('template', 'article')

# Limit
page.children.limit(5)
page.children.offset(10).limit(5)
```
