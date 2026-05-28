# Laws of UX: Complete Reference

Psychological principles that predict user behavior. Understanding these helps design interfaces that work *with* human cognition, not against it.

---

## Cognitive Laws

### Miller's Law

> The average person can hold only 7 (±2) items in working memory.

**Implications:**
- Chunk related items into groups of 5-9
- Don't present more than 7 main navigation items
- Break long forms into logical sections
- Use categorization to reduce perceived complexity

**Design patterns:**
- Phone numbers: (555) 123-4567 (3-3-4 chunks)
- Credit card numbers: 4111 1111 1111 1111 (4-4-4-4 chunks)
- Menu categories instead of flat lists

---

### Hick's Law

> The time to make a decision increases with the number and complexity of choices.

**The formula:** RT = a + b × log2(n)
- Where n = number of choices

**Implications:**
- Reduce options to speed decisions
- Use progressive disclosure for complex features
- Highlight recommended options
- Don't paralyze users with choice

**Design patterns:**
- "Most popular" or "Recommended" badges
- Stepped wizards instead of massive forms
- Smart defaults that work for most users
- Tiered pricing (3 options is optimal)

---

### Cognitive Load

> The amount of mental resources needed to understand and interact with an interface.

**Three types:**
1. **Intrinsic:** Complexity inherent to the task
2. **Extraneous:** Complexity added by poor design
3. **Germane:** Effort spent building mental models

**Implications:**
- Eliminate extraneous load ruthlessly
- Simplify intrinsic load where possible
- Invest in germane load (help users learn)

**Design patterns:**
- Minimize decisions per screen
- Use familiar patterns
- Consistent interaction models
- Clear visual hierarchy

---

### Paradox of the Active User

> Users never read manuals but start using software immediately.

**Implications:**
- Design interfaces that are self-evident
- Don't rely on documentation for basic tasks
- Use progressive onboarding
- Make exploration safe (undo, no penalties)

**Design patterns:**
- Empty states that guide action
- Inline hints at point of need
- Safe exploration (undo everything)
- Skippable tutorials

---

## Attention Laws

### Von Restorff Effect (Isolation Effect)

> When multiple similar objects are present, the one that differs from the rest is most likely to be remembered.

**Implications:**
- Make CTAs visually distinct
- Use contrast for important elements
- Don't overuse—one focal point per view
- Difference should be meaningful, not arbitrary

**Design patterns:**
- Primary button stands out from secondary
- Error states visually distinct
- Featured/recommended items highlighted
- Current step emphasized in progress

---

### Serial Position Effect

> Users best remember the first and last items in a series.

**Two components:**
- **Primacy effect:** First items remembered (transferred to long-term memory)
- **Recency effect:** Last items remembered (still in working memory)

**Implications:**
- Put important items first and last
- Critical actions at edges of navigation
- Key information at start and end of content

**Design patterns:**
- Most-used nav items at edges
- Important form fields first
- Summary at end of long content
- Key takeaways at top and bottom

---

### Selective Attention

> Users focus on a subset of stimuli, usually related to their goals.

**Implications:**
- Don't compete with user intent
- Banner blindness is real
- Important elements must be in expected locations
- Interruptions damage experience

**Design patterns:**
- Primary actions in expected locations
- Don't disguise ads as content
- Interruptions only for critical info
- Let users focus on their task

---

## Perception Laws

### Law of Proximity

> Objects near each other tend to be grouped together.

**Implications:**
- Group related elements spatially
- Labels close to their inputs
- Separate unrelated items
- Whitespace creates grouping

**Design patterns:**
- Form labels adjacent to fields
- Related actions grouped
- Card layouts for grouped content
- Section spacing > element spacing

---

### Law of Similarity

> Elements that share visual characteristics are perceived as related.

**Implications:**
- Style related elements consistently
- Different styles = different meaning
- Color, shape, size all create similarity

**Design patterns:**
- Consistent button styles
- Link styling distinct from text
- Icon families with consistent style
- Status colors used consistently

---

### Law of Common Region

> Elements within a boundary are perceived as a group.

**Implications:**
- Use containers to show relationships
- Cards naturally group content
- Borders define sections
- Background colors create regions

**Design patterns:**
- Card-based layouts
- Form field groupings
- Modal boundaries
- Section backgrounds

---

### Law of Uniform Connectedness

> Visually connected elements are perceived as more related than disconnected ones.

**Implications:**
- Use lines, arrows, or paths to show flow
- Visual connections show relationships
- Timelines and progress bars work on this principle

**Design patterns:**
- Stepper components with connectors
- Tree views with lines
- Timeline designs
- Flow diagrams

---

### Law of Pragnanz (Simplicity)

> People perceive and interpret ambiguous images in the simplest form possible.

**Implications:**
- Simple shapes are processed faster
- Complex designs require more effort
- Ambiguity causes confusion
- Favor clarity over cleverness

**Design patterns:**
- Clean icon design
- Clear hierarchy
- Unambiguous controls
- Obvious affordances

---

## Interaction Laws

### Fitts's Law

> The time to acquire a target is a function of the distance to and size of the target.

**The formula:** T = a + b × log2(1 + D/W)
- D = distance to target
- W = width (size) of target

**Implications:**
- Make frequent targets larger
- Position related actions close together
- Edge/corner targets are easier (infinite edge)
- Touch targets minimum 44×44px

**Design patterns:**
- Full-width mobile buttons
- Large touch targets
- Related actions grouped
- Popup menus near trigger

---

### Jakob's Law

> Users spend most of their time on other sites. They prefer your site to work the same way as other sites they already know.

**Implications:**
- Follow conventions before innovating
- Leverage existing mental models
- Innovation has a learning cost
- Consistency trumps uniqueness

**Design patterns:**
- Standard navigation patterns
- Expected icon meanings
- Platform conventions honored
- Industry-specific patterns followed

---

### Doherty Threshold

> Productivity soars when computer and user interact at a pace (<400ms) that ensures neither has to wait.

**Implications:**
- Respond to input within 400ms
- If longer, show progress
- Perceived performance matters
- Optimize bottlenecks

**Design patterns:**
- Optimistic UI updates
- Skeleton screens
- Background processing
- Progress indicators

---

### Postel's Law (Robustness Principle)

> Be liberal in what you accept, and conservative in what you send.

**Implications:**
- Accept input variations gracefully
- Parse user intent, not just exact format
- Output consistently
- Forgive input errors

**Design patterns:**
- Phone number format flexibility
- Case-insensitive search
- Date parsing (multiple formats)
- Trimming whitespace

---

## Motivation Laws

### Goal-Gradient Effect

> The tendency to approach a goal increases with proximity to the goal.

**Implications:**
- Show progress toward completion
- Make goals feel achievable
- Artificial progress can motivate (10% head start)
- Celebrate milestones

**Design patterns:**
- Progress bars
- Completion percentages
- Streaks and milestones
- "Almost there" messaging

---

### Zeigarnik Effect

> People remember uncompleted tasks better than completed ones.

**Implications:**
- Open loops create engagement
- Incomplete profiles prompt completion
- Draft saving reduces abandonment
- Can be manipulated (use ethically)

**Design patterns:**
- "Complete your profile" prompts
- Saved drafts
- Progress indicators
- "Continue where you left off"

**Warning:** Don't exploit this for dark patterns.

---

### Peak-End Rule

> People judge experiences based on how they felt at the peak and at the end, not by the average.

**Implications:**
- Design memorable peak moments
- End interactions positively
- Single bad moment colors whole experience
- Recovery from errors matters

**Design patterns:**
- Delightful success states
- Positive completion messages
- Error recovery that restores confidence
- Surprise and delight moments

---

## Efficiency Laws

### Pareto Principle (80/20 Rule)

> Roughly 80% of effects come from 20% of causes.

**Implications:**
- Focus on the 20% most-used features
- Optimize the most common paths
- Not all features need equal attention
- Prioritize ruthlessly

**Design patterns:**
- Primary actions prominent
- Shortcuts for power features
- Most-used items easily accessible
- Less-used features in submenus

---

### Parkinson's Law

> Work expands to fill the time available for its completion.

**Implications:**
- Deadlines motivate action
- Time limits can improve focus
- Too much time = procrastination
- Constraints enable creativity

**Design patterns:**
- Session timeouts (with warning)
- Limited-time offers (use honestly)
- Auto-save reduces scope anxiety
- Clear time expectations

---

## Memory & Learning

### Tesler's Law (Conservation of Complexity)

> For any system, there is a certain amount of complexity that cannot be reduced.

**Implications:**
- Some complexity is unavoidable
- Decide: user bears it or system bears it
- Simplifying UI may add complexity elsewhere
- Sometimes "simple" UI is harder to use

**Design patterns:**
- Smart defaults absorb complexity
- Progressive disclosure
- Automation of complex tasks
- Well-designed complex interfaces > dumbed-down simple ones

---

### Working Memory

> A cognitive system for temporarily holding and manipulating information.

**Characteristics:**
- Limited capacity (~4 chunks for complex items)
- Short duration (20-30 seconds without rehearsal)
- Easily disrupted by interference

**Implications:**
- Don't require users to remember across screens
- Keep related information visible
- Minimize context switching
- Use recognition over recall

---

### Occam's Razor

> Among competing hypotheses, the simplest is most likely correct. In design: the simplest solution is usually best.

**Implications:**
- Don't add features without clear need
- Question every element's necessity
- Simpler explanations are more believable
- Complexity should justify itself

**Design patterns:**
- Minimalist design
- Single-purpose interfaces
- Clear, simple copy
- Focused feature sets

---

## Application Guidelines

### When Laws Conflict

Laws sometimes point in different directions:
- **Fitts + Aesthetic:** Large buttons vs. visual elegance
- **Jakob's + Innovation:** Convention vs. differentiation
- **Hick's + Flexibility:** Few options vs. power user needs

**Resolution strategies:**
1. Test with real users
2. Prioritize by impact
3. Context determines priority
4. Progressive disclosure often resolves conflicts

### Using Laws in Design Reviews

**Checklist approach:**
1. Identify the interaction being evaluated
2. List relevant laws
3. Check compliance with each
4. Note conflicts and tradeoffs
5. Propose solutions

**Don't:**
- Apply laws rigidly without context
- Use laws to justify predetermined decisions
- Ignore laws when they conflict with preferences
- Forget that laws describe tendencies, not absolutes
