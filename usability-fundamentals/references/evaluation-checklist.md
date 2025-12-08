# Usability Evaluation Checklist

A comprehensive checklist for reviewing interfaces. Each item includes design-friendly solutions that maintain visual quality while solving usability problems.

---

## Information Architecture

### Navigation

- [ ] **Can users find what they need in ≤3 clicks?**
  - *Problem indicator:* Users give up or use search for basic tasks
  - *Design-friendly fix:* Flatten hierarchy; use mega menus that reveal structure elegantly

- [ ] **Is navigation consistent across all pages?**
  - *Problem indicator:* Users get lost when moving between sections
  - *Design-friendly fix:* Global nav remains constant; use breadcrumbs for context

- [ ] **Are labels clear and jargon-free?**
  - *Problem indicator:* Users hover/click wrong items; ask "what does X mean?"
  - *Design-friendly fix:* Test labels with real users; use familiar terms

- [ ] **Does the hierarchy match user mental models?**
  - *Problem indicator:* Users look in wrong category for content
  - *Design-friendly fix:* Card sorting with users; iterate based on search behavior

### Content Organization

- [ ] **Is the most important content visible without scrolling?**
  - *Problem indicator:* High bounce rate; users miss key actions
  - *Design-friendly fix:* Prioritize above-fold; use visual hierarchy to draw down

- [ ] **Is related content grouped logically?**
  - *Problem indicator:* Users compare items that are far apart
  - *Design-friendly fix:* Use Law of Proximity; card-based grouping

- [ ] **Are long pages chunked with clear sections?**
  - *Problem indicator:* Users lose place; abandon long pages
  - *Design-friendly fix:* Visual section breaks; sticky navigation for long forms

---

## Visual Hierarchy

### Emphasis & Attention

- [ ] **Is the primary action immediately visible?**
  - *Problem indicator:* Users don't know what to do next
  - *Design-friendly fix:* Use Von Restorff effect tastefully; single clear CTA

- [ ] **Do visual weights guide attention correctly?**
  - *Problem indicator:* Eye-tracking shows scattered attention
  - *Design-friendly fix:* Size, color, contrast create intended flow

- [ ] **Is there sufficient contrast without harshness?**
  - *Problem indicator:* Users strain to read; or design feels aggressive
  - *Design-friendly fix:* 4.5:1 contrast minimum; soften with carefully chosen colors

### Layout & Space

- [ ] **Does whitespace aid comprehension?**
  - *Problem indicator:* Interface feels cramped or overwhelming
  - *Design-friendly fix:* Generous margins; space defines relationships

- [ ] **Is the layout scannable?**
  - *Problem indicator:* Users read everything to find what they need
  - *Design-friendly fix:* Clear headings; visual anchors; F-pattern awareness

- [ ] **Are visual elements aligned consistently?**
  - *Problem indicator:* Layout feels "off" or unprofessional
  - *Design-friendly fix:* Grid system; consistent baseline; edge alignment

---

## Interaction Design

### Affordances & Signifiers

- [ ] **Are clickable elements obviously clickable?**
  - *Problem indicator:* Users miss links; click non-interactive elements
  - *Design-friendly fix:* Buttons look pressable; links styled distinctly

- [ ] **Do hover/focus states provide clear feedback?**
  - *Problem indicator:* Users unsure if element is interactive
  - *Design-friendly fix:* Subtle state changes; cursor changes on hover

- [ ] **Are touch targets ≥44×44px on mobile?**
  - *Problem indicator:* Mis-taps; frustration on mobile
  - *Design-friendly fix:* Padding increases hit area; doesn't require visual bloat

- [ ] **Can users undo destructive actions?**
  - *Problem indicator:* Fear of clicking; requests to restore data
  - *Design-friendly fix:* Soft delete; undo in toast notifications

### Feedback & Status

- [ ] **Do users know when the system is working?**
  - *Problem indicator:* Re-clicking; abandonment during waits
  - *Design-friendly fix:* Loading states within 100ms; progress for long waits

- [ ] **Is feedback immediate (<400ms)?**
  - *Problem indicator:* Perceived slowness; double submissions
  - *Design-friendly fix:* Optimistic UI; instant visual response

- [ ] **Are success/error states clearly distinguishable?**
  - *Problem indicator:* Users unsure if action worked
  - *Design-friendly fix:* Color + icon + text (never color alone)

---

## Forms & Input

### Labels & Instructions

- [ ] **Are fields labeled clearly?**
  - *Problem indicator:* Users enter wrong information
  - *Design-friendly fix:* Persistent labels above fields; never just placeholder

- [ ] **Are placeholder text and labels distinct?**
  - *Problem indicator:* Users lose context when typing
  - *Design-friendly fix:* Placeholder = example; label = field name

- [ ] **Are required fields marked appropriately?**
  - *Problem indicator:* Form errors on submit; user frustration
  - *Design-friendly fix:* Mark optional fields instead (fewer required markers)

### Validation & Errors

- [ ] **Is validation inline and real-time?**
  - *Problem indicator:* Error avalanche on submit
  - *Design-friendly fix:* Validate on blur; gentle corrections

- [ ] **Are errors helpful, not punitive?**
  - *Problem indicator:* Users feel scolded; abandon form
  - *Design-friendly fix:* Explain what's wrong AND how to fix it

- [ ] **Do inputs have appropriate types?**
  - *Problem indicator:* Wrong keyboard on mobile; awkward input
  - *Design-friendly fix:* type="email", "tel", "number" as appropriate

### Input Assistance

- [ ] **Are smart defaults provided?**
  - *Problem indicator:* Users must fill obvious fields
  - *Design-friendly fix:* Pre-fill from context; most common options first

- [ ] **Is input format forgiving?**
  - *Problem indicator:* Format errors for reasonable input
  - *Design-friendly fix:* Accept multiple formats; display in one

- [ ] **Does autocomplete/autosuggest reduce effort?**
  - *Problem indicator:* Typing the same things repeatedly
  - *Design-friendly fix:* Browser autocomplete enabled; custom suggestions

---

## Consistency

### Visual Consistency

- [ ] **Are similar elements styled consistently?**
  - *Problem indicator:* Users unsure if elements are equivalent
  - *Design-friendly fix:* Design system; consistent component library

- [ ] **Do colors have consistent meaning?**
  - *Problem indicator:* Red used for both error AND feature highlight
  - *Design-friendly fix:* Semantic color system; reserved meanings

- [ ] **Is typography consistent throughout?**
  - *Problem indicator:* Multiple fonts; inconsistent sizing
  - *Design-friendly fix:* Type scale; limited font variations

### Behavioral Consistency

- [ ] **Do icons have consistent meaning?**
  - *Problem indicator:* Same icon means different things
  - *Design-friendly fix:* Icon audit; one meaning per icon

- [ ] **Are interactions predictable?**
  - *Problem indicator:* Same gesture produces different results
  - *Design-friendly fix:* Consistent interaction patterns

- [ ] **Does terminology remain stable?**
  - *Problem indicator:* "Project" here, "Workspace" there for same concept
  - *Design-friendly fix:* Content audit; single term per concept

---

## Accessibility (Usability Foundation)

*Note: Not WCAG compliance, but foundational usability that benefits everyone*

### Perceivable

- [ ] **Is text readable at default size?**
  - *Problem indicator:* Users zoom; complaints about small text
  - *Design-friendly fix:* 16px minimum body; generous line height

- [ ] **Does color convey meaning with additional cues?**
  - *Problem indicator:* Colorblind users miss states
  - *Design-friendly fix:* Color + icon + text

- [ ] **Is there sufficient contrast?**
  - *Problem indicator:* Readability issues; eye strain
  - *Design-friendly fix:* Test with contrast checker; 4.5:1 minimum

### Operable

- [ ] **Can the interface be used with keyboard only?**
  - *Problem indicator:* Focus gets lost; can't reach elements
  - *Design-friendly fix:* Visible focus states; logical tab order

- [ ] **Are focus states visible?**
  - *Problem indicator:* Keyboard users can't see where they are
  - *Design-friendly fix:* Custom focus styles that match design

### Understandable

- [ ] **Is language simple and clear?**
  - *Problem indicator:* Users don't understand instructions
  - *Design-friendly fix:* Plain language; avoid jargon

- [ ] **Is behavior predictable?**
  - *Problem indicator:* Unexpected outcomes; surprises
  - *Design-friendly fix:* Follow conventions; announce changes

---

## Error Handling

### Prevention

- [ ] **Are error-prone conditions eliminated?**
  - *Problem indicator:* Same errors occur repeatedly
  - *Design-friendly fix:* Constraints prevent invalid input

- [ ] **Are dangerous actions confirmed?**
  - *Problem indicator:* Accidental deletions; irreversible mistakes
  - *Design-friendly fix:* Confirmation for destructive actions; undo for others

- [ ] **Are constraints visible before errors occur?**
  - *Problem indicator:* Users discover limits only after violation
  - *Design-friendly fix:* Character counters; format hints; available options

### Recovery

- [ ] **Do error messages explain the problem clearly?**
  - *Problem indicator:* "An error occurred" messages
  - *Design-friendly fix:* Specific explanation in plain language

- [ ] **Do error messages suggest solutions?**
  - *Problem indicator:* Users don't know how to proceed
  - *Design-friendly fix:* "Try X" or direct action link

- [ ] **Is the error location highlighted?**
  - *Problem indicator:* Users can't find what needs fixing
  - *Design-friendly fix:* Scroll to and highlight the problem field

---

## Performance (Perceived Usability)

### Response Time

- [ ] **Does UI respond within 100ms?**
  - *Problem indicator:* Interface feels sluggish
  - *Design-friendly fix:* Immediate visual feedback; process in background

- [ ] **Do operations complete within 1 second?**
  - *Problem indicator:* Users lose focus; repeat actions
  - *Design-friendly fix:* Optimize; or show progress

- [ ] **Are long operations shown with progress?**
  - *Problem indicator:* Users think system is frozen
  - *Design-friendly fix:* Progress indicator; time estimates

### Loading States

- [ ] **Are loading states informative?**
  - *Problem indicator:* Generic spinner provides no context
  - *Design-friendly fix:* Skeleton screens; progress percentage

- [ ] **Does content load progressively?**
  - *Problem indicator:* Blank page until everything loads
  - *Design-friendly fix:* Priority loading; above-fold first

- [ ] **Is layout stable during load?**
  - *Problem indicator:* Content shifts; mis-clicks
  - *Design-friendly fix:* Reserve space; fixed dimensions

---

## Mobile Usability

### Touch Interaction

- [ ] **Are touch targets adequately sized?**
  - *Problem indicator:* Mis-taps; frustration
  - *Design-friendly fix:* 44px minimum; 48px recommended

- [ ] **Is there adequate space between targets?**
  - *Problem indicator:* Wrong target hit
  - *Design-friendly fix:* 8px minimum between touchable elements

- [ ] **Are primary actions in thumb-reach zones?**
  - *Problem indicator:* Two-handed operation required
  - *Design-friendly fix:* Important actions bottom of screen; reachable areas

### Content Adaptation

- [ ] **Is content readable without zooming?**
  - *Problem indicator:* Pinch-zoom required
  - *Design-friendly fix:* Responsive typography; viewport-aware sizing

- [ ] **Are forms easy to complete on mobile?**
  - *Problem indicator:* Form abandonment on mobile
  - *Design-friendly fix:* Appropriate input types; minimal fields; autofill

- [ ] **Does horizontal scrolling ever occur?**
  - *Problem indicator:* Content extends beyond viewport
  - *Design-friendly fix:* True responsive design; fluid layouts

---

## Severity Rating Scale

When documenting issues, assign severity:

| Rating | Label | Description | Priority |
|--------|-------|-------------|----------|
| 0 | None | Not a usability problem | N/A |
| 1 | Cosmetic | Minor issue; fix if time allows | Low |
| 2 | Minor | Small hindrance; users work around it | Medium |
| 3 | Major | Significant barrier; causes errors/abandonment | High |
| 4 | Critical | Blocks task completion; must fix immediately | Critical |

---

## Review Process

### Preparation
1. Define user personas and key tasks
2. Identify pages/flows to evaluate
3. Gather checklist items relevant to scope

### Evaluation
1. Walk through as each persona
2. Attempt each key task
3. Note issues with location, description, severity
4. Capture screenshots of problems

### Documentation
1. Organize findings by page/flow
2. Group by severity
3. Include recommendations (not just problems)
4. Prioritize for development roadmap

### Follow-up
1. Track fixes implemented
2. Re-evaluate changed areas
3. Monitor analytics for improvement
4. Repeat evaluation periodically
