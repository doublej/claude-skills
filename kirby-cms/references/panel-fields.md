# Panel Field Reference

All available Panel field types with usage examples.

## Text Input Fields

### text

Single-line text input.

```yaml
title:
  type: text
  label: Title
  placeholder: Enter title...
  required: true
  maxlength: 100
  counter: true
  icon: title
  before: Title:
  after: chars
```

### textarea

Multi-line text input.

```yaml
description:
  type: textarea
  label: Description
  maxlength: 500
  buttons:
    - bold
    - italic
    - link
  size: medium  # small, medium, large, huge
```

### writer

Rich text editor (inline formatting).

```yaml
bio:
  type: writer
  label: Biography
  inline: true
  marks:
    - bold
    - italic
    - link
    - code
```

### blocks

Block-based content editor.

```yaml
content:
  type: blocks
  label: Page Content
  fieldsets:
    - heading
    - text
    - image
    - gallery
    - video
    - quote
    - code
    - list
```

### list

Simple list field.

```yaml
features:
  type: list
  label: Features
```

---

## Selection Fields

### select

Dropdown selection.

```yaml
category:
  type: select
  label: Category
  options:
    news: News
    blog: Blog Post
    tutorial: Tutorial
  default: blog
  empty: Select a category...
```

Dynamic options:

```yaml
author:
  type: select
  options: query
  query: site.users
  text: "{{ user.name }}"
  value: "{{ user.email }}"
```

### multiselect

Multiple selection dropdown.

```yaml
tags:
  type: multiselect
  label: Tags
  options:
    - php
    - javascript
    - css
    - design
  max: 5
  search: true
```

### radio

Single choice radio buttons.

```yaml
status:
  type: radio
  label: Status
  options:
    draft: Draft
    review: In Review
    published: Published
  default: draft
```

### checkboxes

Multiple checkboxes.

```yaml
features:
  type: checkboxes
  label: Features
  options:
    responsive: Responsive Design
    seo: SEO Optimized
    fast: Fast Loading
```

### toggle

Boolean on/off switch.

```yaml
featured:
  type: toggle
  label: Featured
  text:
    - "No"
    - "Yes"
  default: false
```

### toggles

Multiple toggle options (single selection).

```yaml
layout:
  type: toggles
  label: Layout
  options:
    - value: left
      text: Left
      icon: align-left
    - value: center
      text: Center
      icon: align-center
    - value: right
      text: Right
      icon: align-right
  default: left
```

### tags

Free-form tag input.

```yaml
keywords:
  type: tags
  label: Keywords
  accept: options  # or 'all'
  options:
    - design
    - development
    - marketing
  max: 10
  separator: ","
```

---

## Date & Time Fields

### date

Date picker.

```yaml
publishDate:
  type: date
  label: Publish Date
  default: today
  min: 2020-01-01
  max: 2030-12-31
  display: DD.MM.YYYY
```

### time

Time picker.

```yaml
eventTime:
  type: time
  label: Event Time
  default: now
  step: 15  # minutes
```

---

## Number Fields

### number

Numeric input.

```yaml
price:
  type: number
  label: Price
  min: 0
  max: 10000
  step: 0.01
  before: $
```

### range

Slider input.

```yaml
rating:
  type: range
  label: Rating
  min: 0
  max: 5
  step: 0.5
  default: 3
```

---

## Link & URL Fields

### url

URL input with validation.

```yaml
website:
  type: url
  label: Website
  placeholder: https://example.com
```

### email

Email input with validation.

```yaml
contactEmail:
  type: email
  label: Contact Email
```

### tel

Phone number input.

```yaml
phone:
  type: tel
  label: Phone Number
```

### link

Link selector (internal/external).

```yaml
cta:
  type: link
  label: Call to Action
  options:
    - page
    - url
    - email
    - tel
```

---

## Relation Fields

### pages

Page selector.

```yaml
relatedPages:
  type: pages
  label: Related Pages
  max: 5
  query: site.find('blog').children.listed
  layout: list  # or 'cards'
  info: "{{ page.date.toDate('Y-m-d') }}"
```

### files

File selector/uploader.

```yaml
gallery:
  type: files
  label: Gallery
  layout: cards
  size: small  # tiny, small, medium, large, huge
  uploads:
    parent: site
    template: image
  query: page.images
  max: 10
```

### users

User selector.

```yaml
author:
  type: users
  label: Author
  max: 1
  default: true  # current user
```

### entries

Generic relation picker (pages + files).

```yaml
references:
  type: entries
  label: References
  layout: list
  max: 10
```

---

## Special Fields

### color

Color picker.

```yaml
brandColor:
  type: color
  label: Brand Color
  default: "#ff0000"
  mode: hex  # hex, rgb, hsl
  alpha: true
```

### slug

URL slug field.

```yaml
slug:
  type: slug
  label: URL Slug
  sync: title
  allow: a-z0-9-
```

### structure

Repeatable field groups.

```yaml
team:
  type: structure
  label: Team Members
  fields:
    name:
      type: text
      label: Name
    role:
      type: text
      label: Role
    photo:
      type: files
      max: 1
```

### object

Single object with fields.

```yaml
address:
  type: object
  label: Address
  fields:
    street:
      type: text
    city:
      type: text
    zip:
      type: text
```

### layout

Column layout builder.

```yaml
pageLayout:
  type: layout
  label: Page Layout
  layouts:
    - "1/1"
    - "1/2, 1/2"
    - "1/3, 1/3, 1/3"
    - "1/4, 3/4"
  fieldsets:
    - heading
    - text
    - image
```

---

## Display Fields (Non-Input)

### headline

Section heading.

```yaml
sectionTitle:
  type: headline
  label: SEO Settings
  numbered: false
```

### info

Informational text.

```yaml
help:
  type: info
  label: Help
  text: |
    This page uses the **article** template.
    [View documentation](https://docs.example.com)
  theme: info  # info, positive, negative, warning, none
```

### line

Visual separator.

```yaml
separator:
  type: line
```

### gap

Empty spacing.

```yaml
spacer:
  type: gap
```

### stats

Display statistics.

```yaml
pageStats:
  type: stats
  reports:
    - label: Children
      value: "{{ page.children.count }}"
    - label: Files
      value: "{{ page.files.count }}"
```

### hidden

Store data without display.

```yaml
internalId:
  type: hidden
  default: "{{ page.uuid }}"
```

---

## Field Properties Reference

Common properties available on most fields:

```yaml
fieldName:
  type: text
  label: Field Label         # Display label
  help: Some help text       # Help tooltip
  placeholder: Enter...      # Placeholder text
  default: Default value     # Default value
  required: true             # Mark as required
  disabled: true             # Make read-only
  translate: false           # Disable translation
  width: 1/2                 # Column width (1/4, 1/3, 1/2, 2/3, 3/4, 1/1)
  when:                      # Conditional display
    otherField: value
  before: Prefix             # Text before field
  after: Suffix              # Text after field
  icon: edit                 # Icon name
```

## Field Method Access

In templates, access field values:

```php
// Raw value
$page->title()->value()

// Processed
$page->text()->kirbytext()
$page->date()->toDate('F j, Y')
$page->gallery()->toFiles()
$page->author()->toUser()
$page->tags()->split(',')
$page->price()->toFloat()
$page->featured()->toBool()

// Structure fields
foreach($page->team()->toStructure() as $member):
    echo $member->name();
endforeach;

// Check if empty
if($page->text()->isNotEmpty()):
    echo $page->text();
endif;
```
