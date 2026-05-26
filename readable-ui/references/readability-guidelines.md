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

## Source Notes

This skill is based on the same core evidence used by major design systems and accessibility guidance:

- WCAG contrast, resize, and text spacing guidance
- Material, Fluent, Carbon, GOV.UK, and USWDS typography conventions
- Baymard form-label guidance
- Nielsen Norman Group research on scanning, grouping, and cognitive load
