# Construction Formulas

Detailed formulas for mathematical logo construction. SKILL.md has summaries; this file has full derivations.

## Tangent Fillet (Rounded Corner)

Two lines meeting at vertex `V` with interior angle `θ` (0 < θ < π), desired fillet radius `r`.

```
t = r × cot(θ/2)       tangent point distance along each line from V
d = r / sin(θ/2)        fillet center distance from V along angle bisector
```

The arc sweeps from one tangent point to the other. SVG arc command:
```
A r r 0 0 [sweep] x2 y2
```
where `sweep` = 1 for clockwise fillet, 0 for counter-clockwise.

### Special cases
- Right angle (θ = π/2): `t = r`, `d = r√2`
- 60° angle: `t = r√3`, `d = 2r`
- 120° angle: `t = r/√3`, `d = 2r/√3`

## Circle Tangent to Two Circles

Find circle of radius `r` tangent externally to `(C1, R1)` and `(C2, R2)`.

### External-external tangency
1. Inflate: `R1' = R1 + r`, `R2' = R2 + r`
2. Center of unknown circle lies at intersection of:
   - Circle centered at `C1` with radius `R1'`
   - Circle centered at `C2` with radius `R2'`
3. Solve: let `d = |C2 - C1|`
   ```
   a = (R1'^2 - R2'^2 + d^2) / (2d)
   h = √(R1'^2 - a^2)
   ```
   Midpoint `M = C1 + a × (C2 - C1) / d`
   Two solutions: `M ± h × perpendicular_unit_vector`

### Internal tangency
Use `R' = |R - r|` instead of `R + r` for the circle that contains the new one.

### No solution
If `d > R1' + R2'` (too far apart) or `d < |R1' - R2'|` (one inside other), no tangent circle of that radius exists at that configuration.

## Arc Tangent to Line + Circle

Find arc of radius `r` tangent to line `L` and circle `(C, R)`.

1. Offset line `L` by distance `r` in the desired direction → line `L'`
2. Inflate circle: `R' = R + r` (external) or `R' = |R - r|` (internal)
3. Center = intersection of `L'` and circle `(C, R')`

## Bézier Continuity

### G0 (positional)
Segments share an endpoint. Always required.

### G1 (tangent / direction)
At shared point `P` between segment 1 `(..., P2, P3=P)` and segment 2 `(Q0=P, Q1, ...)`:
```
(P3 - P2) × (Q1 - Q0) = 0    (cross product = 0, i.e. collinear)
(P3 - P2) · (Q1 - Q0) > 0    (same direction, not reversed)
```

### C1 (tangent + speed)
Stronger than G1. Enforce:
```
Q1 = Q0 + (P3 - P2)
```
The outgoing handle mirrors the incoming handle exactly.

### G2 (curvature)
Curvature matches at the join. For cubic Béziers, this constrains both Q1 and Q2:
```
κ1(t=1) = κ2(t=0)
```
Rarely needed for logos — G1 is usually sufficient.

## Circle Approximation with Cubic Béziers

Quarter-arc from `(1, 0)` to `(0, 1)` on unit circle:

```
k = 4(√2 - 1) / 3 ≈ 0.55228475

P0 = (1, 0)
P1 = (1, k)
P2 = (k, 1)
P3 = (0, 1)
```

Maximum radial error: ~0.027% (negligible for all logo sizes).

Full circle = 4 quarter-arcs. For circle at `(cx, cy)` with radius `r`:
```
M cx+r cy
C cx+r cy+k*r, cx+k*r cy+r, cx cy+r
C cx-k*r cy+r, cx-r cy+k*r, cx-r cy
C cx-r cy-k*r, cx-k*r cy-r, cx cy-r
C cx+k*r cy-r, cx+r cy-k*r, cx+r cy
Z
```

## Polar Fourier Curves

General form for n-fold symmetric marks:
```
r(θ) = R0 + Σ(k=1..K) a_k × cos(k × n × θ)
```

- `R0`: base radius
- `n`: symmetry order (lobe count)
- `a_k`: amplitude of k-th harmonic
- `K`: number of harmonics (keep low: 1-2 for logos)

Convert to Cartesian: `x = r(θ)cos(θ)`, `y = r(θ)sin(θ)`

Discretise with enough points (e.g., 360) and fit cubic Béziers through the points, enforcing G1 at joins.

## Superellipse

```
|x/a|^p + |y/b|^p = 1
```

- `p = 2`: ellipse
- `p = 2.5`: typical "squircle" (iOS icon shape)
- `p → ∞`: rectangle
- `p < 2`: astroid-like (pinched)

Parametric form: `x = a × sgn(cos θ) × |cos θ|^(2/p)`, `y = b × sgn(sin θ) × |sin θ|^(2/p)`
