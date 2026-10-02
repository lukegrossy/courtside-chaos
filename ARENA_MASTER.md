# Canonical Arena Master

This is the reusable spatial master for every arena cutscene in Courtside Chaos.

## Files

- `assets/templates/arena-master.svg` — neutral 853 × 1844 arena plate with locked court/camera geometry.
- `assets/templates/arena-guides.svg` — transparent guide overlay for generated/painted arena art.

These files are production guides, not player-facing screens.

## Locked geometry

- Canvas: **853 × 1844**
- Court centre: **x 426.5**
- Half-court line: **y 1160**
- Centre circle: **x 426.5, y 1160**
- Centre-circle ellipse: **176 × 92**
- Far baseline: **y 650**
- Near baseline: **y 1680**
- Sidelines converge from near corners toward the far court.
- One basket belongs to each end of the court.
- No centre-court logo.
- No foreground audience may overlap the playable/action floor.

## Camera

Fixed elevated arena camera. The viewer should feel seated high enough to understand the space, but close enough that a human-sized subject at centre court remains readable on an iPhone.

Do not change camera height or lens between arena gag scenes unless a story absolutely requires it.

## Action zone

The green rectangle in `arena-guides.svg` is the preferred subject zone. Doris, Sam, the referee, Gordy, the dog, presenters, players and props should generally remain inside it.

The cyan rectangle is the broader readable floor zone.

## Crowd

- Crowd belongs in stands and at the court edge.
- No foreground heads or bodies may obscure the floor.
- Dense crowd is encouraged, but detail should recede with depth.
- Crowd density must not distort court dimensions.

## Court validation before art approval

Every arena scene must pass all of these before comedy/art polish:

1. Half-court line passes through the exact centre of the centre circle.
2. Centre circle remains at the same coordinates and apparent scale.
3. Three-point arcs exist and belong to their baskets.
4. Backboard/hoop remains attached to the court end, never the stands.
5. Players/subjects share one consistent physical scale.
6. Feet remain visible for full-body action.
7. No accidental second court markings or stray lines.
8. No readable generated signage/logos unless deliberately added later in code or hand-authored art.

## Rendering target

The SVG is deliberately simple. Final art should be repainted/re-rendered into the established Courtside Chaos visual family:

- dense ordered-looking VGA dithering
- warm practical arena lighting
- dark northern palette
- believable 1980s building materials
- weathered adult faces
- polished wood with restrained highlights
- no glossy modern-game treatment

Use the geometry as the skeleton; use `chainsaw.webp` and the strongest shipped cutscenes as the rendering reference.
