# Readability Guidelines

## Working Principle

Readable UI is mostly a product of hierarchy, spacing, contrast, and clear copy. Font taste matters less than whether users can quickly identify what is important, what belongs together, and what they should do next.

## Typography Defaults

- Default body text should usually be at least 16px on web.
- Long-form reading often feels better at 17 to 20px.
- Body line height should usually sit between 1.45 and 1.65.
- Use no more than 1 to 2 type families and a small set of weights.
- Prefer stable, familiar fonts over decorative or thin styles for core UI.
- Define semantic roles such as page title, section heading, body, label, caption, helper text, button, table cell, and error.

## Spacing and Measure

- Keep related items close and unrelated groups apart.
- Use a consistent spacing scale.
- For long-form text, constrain width to about 60 to 75 characters per line.
- Avoid full-width paragraphs on large screens.
- Increase space above a section more than the gap between a heading and its content.

## Contrast

- Normal text should meet at least 4.5:1 contrast.
- Large text should meet at least 3:1 contrast.
- Use semantic text colors instead of pale gray by default.
- Treat borders and component boundaries as functional, not decorative.
- Verify the design on the real background, not just in isolation.

## Scannability

- Headings should be specific and descriptive.
- Important words should appear early in a label or sentence.
- Keep paragraphs short.
- Use bullets for parallel information.
- Make status and next steps visible without extra digging.

## Forms

- Labels should stay visible after typing.
- Place labels above inputs.
- Put helper text near the field it explains.
- Put validation errors next to the field and summarize when the form is long.
- Never use placeholder text as the only label.
- Preserve user input after validation errors.

## Buttons and Links

- Buttons should state the action, and often the object.
- Links should describe the destination.
- Destructive actions should name the consequence.
- Avoid vague labels such as OK, Submit, or Continue when the next step is not obvious.

## Dense Dashboards

- Keep labels smaller and less prominent than values, but still readable.
- Align numbers consistently.
- Use tabular numerals where useful.
- Separate metadata from actions.
- Do not encode meaning with color alone.

## Long-Form Content

- Use short paragraphs and descriptive headings.
- Include examples after rules.
- Keep code blocks and technical snippets easy to scan.
- Use a table of contents when the page is long.

## Practical Review Checklist

- Can the page be understood by scanning headings, labels, values, and actions?
- Is the body text comfortable to read without zooming?
- Are related elements visually grouped?
- Do labels remain visible and descriptive?
- Are errors specific and fixable?
- Is the primary action clear?
- Does the layout still work with increased text spacing?
- Is contrast strong enough for normal reading?

## Concrete Examples

Start from `assets/tokens.css` for a contrast-safe type, spacing, and color scale, then tune to the brand.

### Form field

Bad — placeholder is the only label, error is vague and far from the field:

```html
<input type="email" placeholder="Email">
<p class="form-error">Invalid input.</p>
```

Good — persistent label above, helper near the field, specific inline error, input preserved:

```html
<label class="label" for="email">Work email</label>
<input class="body" id="email" type="email" value="ana@" aria-describedby="email-help email-err">
<p class="helper" id="email-help">We use this to send your receipt.</p>
<p class="error" id="email-err">Add the part after @, e.g. ana@acme.com.</p>
```

### Button label

Bad: `OK` · `Submit` · `Continue` (action and object unclear).
Good: `Create account` · `Delete 3 invoices` · `Save draft` (verb + object; consequence named).

### Dashboard metric

Bad — value and label compete; number is non-tabular; meaning is color-only:

```html
<div><span style="font-size:16px;color:#999">Revenue</span>
     <span style="font-size:16px;color:green">$12,480 ▲</span></div>
```

Good — value dominates, label is muted but readable, tabular numerals, direction has a word:

```html
<div class="metric">
  <div class="metric-value">$12,480</div>
  <div class="metric-label">Revenue · up 8% vs last week</div>
</div>
```

## Source Notes

Based on WCAG (contrast, resize, text-spacing), Material/Fluent/Carbon/GOV.UK/USWDS typography conventions, Baymard form-label research, and NN/g work on scanning and cognitive load.
