# Canonical Arena Master

This document locks the **Lumberjack Shack** as the arena used throughout Courtside Chaos Season 1.

The two accepted raster views define what the building looks and feels like. The SVG files define the court geometry. When a generated raster contains a minor accidental line or marking that conflicts with the geometry rules below, **the geometry rules win**.

## Canonical files

### Visual / architecture masters

- `assets/templates/shack_arena_master_wide.webp` — canonical wide arena view.
- `assets/templates/shack_arena_master_behind_basket.webp` — canonical behind-the-basket view.

These two images lock:

- arena size and crowd scale
- exposed roof-truss architecture
- wall materials and blue lower-wall treatment
- warm industrial lighting
- worn hardwood treatment
- seating density and proximity to the floor
- simple period scoreboard character
- general basket/backboard construction
- overall VGA palette, dithering and atmosphere

Future arena scenes change the **event**, not the building.

### Spatial / court masters

- `assets/templates/arena-master.svg` — neutral 853 × 1844 court/camera geometry.
- `assets/templates/arena-guides.svg` — transparent alignment/action-zone overlay.

These files govern court markings and spatial relationships.

## Building and lore lock

The Shack is a modest, well-used semi-pro basketball building in an unnamed North Country city in 1984.

It is **not** an NBA arena and must never drift toward one.

- mid-size local building, not a major-league bowl
- somewhat struggling semi-pro/minor-league operation
- packed local support can make it feel loud without making the building physically huge
- exposed steel/wood roof structure and practical industrial lamps
- worn institutional walls, railings, seating and scorer's table
- simple older scoreboard: HOME, VISITOR, clock, score and period only
- no giant video board, ribbon screens or sophisticated graphics
- no championship banners or invented historical achievements
- no city name
- no invented sponsor branding or readable generated lore
- no luxury suites or modern NBA architecture

The building should feel loved, useful and slightly behind the times.

## Locked court geometry

- Canvas: **853 × 1844**
- Court centre: **x 426.5**
- The half-court line is the **single transverse sideline-to-sideline line** through the exact centre of the centre circle.
- Never draw a longitudinal white line running from one basket/key, through centre court, toward the other basket/key.
- Centre circle stays geometrically centred and consistent between camera angles.
- Three-point markings must belong to their respective baskets and remain internally consistent.
- Lane/key treatment should read as period-appropriate early-1980s semi-pro basketball, not a modern NBA court.
- No modern restricted-area semicircle treatment unless historically/story specifically justified.
- One basket belongs to each end of the court.
- No centre-court logo.
- No random extra floor markings or decorative timber clutter.
- No foreground audience may overlap the playable/action floor.

The accepted raster masters are visual references, not permission to reproduce an accidental generated court-line artifact.

## Camera lock

Two camera families are now canonical.

### Wide arena angle

Use `shack_arena_master_wide.webp` for full-building establishing shots, centre-court gags, mascot performances, and Doris/referee/dog/Gordy staging where broad spatial context matters.

Preserve its arena proportions, crowd scale, rafters, lighting, wall height and modest building size.

### Behind-the-basket angle

Use `shack_arena_master_behind_basket.webp` for basket-end action, free throws, game-night moments where the near hoop is part of the composition, and alternate cutaways requiring depth down the floor.

It is the **same building**, not a second arena. Scoreboard style, wall treatment, crowd density, rafters, lighting, paint colours and court proportions must agree with the wide view.

Do not independently redesign architecture when changing camera angle.

## Action zone

The green rectangle in `arena-guides.svg` is the preferred subject zone. Doris, Sam, the referee, Gordy, the dog, presenters, players and props should generally remain inside it.

The cyan rectangle is the broader readable floor zone.

## Crowd

- Crowd belongs in stands and at the court edge.
- Dense crowds are encouraged, but the Shack must remain visibly modest in capacity.
- Detail should recede with depth.
- Crowd density must never distort court dimensions.
- Avoid oversized foreground spectators that turn a cutscene into a crowd poster instead of a basketball scene.
- Front-row spectators should sit naturally close to the floor without blocking the action.

## Court validation before art approval

Every arena scene must pass these checks before comedy/art polish:

1. Half-court line runs sideline-to-sideline through the exact centre of the centre circle.
2. There is **no** longitudinal line connecting the two halves of the court.
3. Centre circle remains consistent in position and apparent scale for the chosen camera.
4. Three-point markings exist where required and belong to the correct basket.
5. Key/lane geometry reads as early-1980s semi-pro, not modern NBA.
6. Backboard and hoop physically belong to the court, never the stands.
7. Players/subjects share one believable physical scale.
8. Feet remain visible for full-body action.
9. No accidental second court markings, stray lines or centre logo.
10. No invented championship banners, city name or generated arena lore.

## Rendering target

Final arena art must remain in the established Courtside Chaos family:

- dense ordered-looking VGA dithering
- warm practical arena lighting
- dark northern palette
- believable 1980s building materials
- weathered adults
- polished but worn hardwood
- restrained highlights
- no glossy modern-sports presentation
- no NBA-scale spectacle

Use the canonical raster angles for the Shack's appearance, the SVG geometry for court correctness, and `chainsaw.webp` plus the strongest shipped cutscenes for character/rendering quality.
