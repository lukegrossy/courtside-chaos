# Courtside Chaos — Visual Bible

This document is the production visual source of truth for Season 1.

The repository itself is authoritative. New artwork should be judged against the shipped dashboard, portraits and strongest cutscenes — not against a generic "retro" or "pixel art" description.

## 1. Master stage

**All full-screen game art is authored for exactly 853 × 1844 px.**

That is the game stage. Treat it as the master canvas.

Do not use ordinary 9:16 artwork and rely on CSS to crop it. A 9:16 image is materially wider than the game stage, and `object-fit: cover` removes significant composition from both sides.

For every new cutscene:

- compose directly at 853 × 1844
- keep the visual joke readable at phone size
- keep faces, hands, props and court geometry away from crop-risk edges
- use a fixed camera unless the scene specifically requires movement
- do not add foreground crowd that blocks the court
- confirm the basketball court reads correctly before adding the gag

The dashboard frame, decision screen and moment screen are already exact 853 × 1844 masters and should not be casually resized.

## 2. Primary reference assets

### Dashboard/material language

Use these as the source of truth for physical materials and UI texture:

- `assets/ui/frame.webp`
- `assets/ui/decision.webp`
- `assets/ui/moment.webp`
- `assets/ui/gazette.webp`
- `assets/ui/courtside-header.png`
- `assets/ui/lumberjack-footer.png`

The visual language is:

- black desk/felt
- aged cream lined paper
- worn metal/brass edging
- tape, pins and physical stationery
- institutional newspaper stock
- restrained shadows that make paper feel physically layered
- no glossy modern-app cards
- no neon gradients
- no generic SaaS UI

### Sandra

Core master:

- `assets/portraits/sandra/base.webp`

Strong environment references:

- `assets/portraits/sandra/sandra_home_arena.webp`
- `assets/portraits/sandra/sandra_gasstation.webp`
- `assets/portraits/sandra/sandra_playoff_road.webp`
- `assets/portraits/sandra/sandra_awards.webp`

Sandra is the visual anchor of the entire game.

For ordinary background/environment changes, preserve her identity, facial proportions, hair shape and pose as closely as possible. Wardrobe/expression changes should happen only when the story calls for them.

She should read as:

- adult
- observant
- competent
- restrained
- mildly unimpressed more often than cheerful
- unmistakably the same person from image to image

Avoid glamour posing or broad generic smiles.

### Cutscene quality references

Use these as the target family:

- `assets/cutscenes/chainsaw.webp`
- `assets/cutscenes/radio.webp`
- `assets/cutscenes/crate.webp`
- `assets/cutscenes/boxes.webp`
- `assets/cutscenes/tipoff_road.webp`
- `assets/cutscenes/hotdish_team.webp`

The target is polished early-1990s VGA adventure-game illustration: dense ordered-looking dithering, strong silhouettes, warm practical lighting, weathered adults, readable props and a slightly heightened but grounded world.

Do not smooth this into generic digital painting.

### Lumberjack Shack / arena

Canonical visual angle masters:

- `assets/templates/shack_arena_master_wide.webp`
- `assets/templates/shack_arena_master_behind_basket.webp`

Canonical court geometry:

- `assets/templates/arena-master.svg`
- `assets/templates/arena-guides.svg`

The raster masters lock the Shack's architecture, modest semi-pro scale, crowd density, industrial rafters, worn hardwood, blue/cream institutional materials, practical lighting and simple period scoreboard. The SVG files lock the court geometry.

The Shack is a somewhat struggling 1984 semi-pro building in an unnamed North Country city — **not an NBA arena**. Do not add championship banners, luxury/major-league architecture, a sophisticated video scoreboard, a city name or invented arena lore.

**Signage rule: less is more.** One strong arena identity sign is enough. Do not fill blank walls or forecourt space with extra slogans, repeated team branding, civic mottos or decorative copy such as “JACKS PLAY HERE” unless a story specifically requires it. Empty, weathered architecture is part of the visual language.

When a raster reference contains a minor generated floor-line artifact, the documented court geometry takes precedence.

Exterior continuity is also locked:

- `assets/templates/shack_exterior_master_pre_blob.mp4` — exterior before Ricky's statue story
- `assets/templates/shack_exterior_master_post_blob.webp` — exterior after the Blob exists

Once `S.flags.blob` is true, THE BLOB is permanent exterior canon: the lumpy abstract bronze on a low granite plinth, plaque **MOMENTUM — #33**. Later exterior Shack art must not revert to the pre-Blob state. The building remains the same building; only the permanent landmark changes.

### Promotional exception

`assets/ui/cover.webp` is deliberately more like painted box/poster art.

It is a marketing/title-image exception, not the rendering target for every in-game scene.

## 3. Palette

Current production tokens from `index.html`:

- green: `#1c5424`
- blue: `#27506e`
- amber: `#7a4210`
- red: `#9a3826`
- ink: `#18140f`
- label: `#2c2820`
- subtext: `#3f382e`
- cream: `#efe6d2`

These are interface anchors, not a rule that every illustration must use only these colours.

Artwork should generally live in muted northern winter / wood / tungsten / institutional tones, with saturated colour used deliberately.

## 4. Typography hierarchy

The shipped game uses a deliberate mixed editorial/office hierarchy:

- **Courier New / monospace** — Sandra notes, operational text, decision copy, metrics
- **Arial Black / heavy condensed sans** — labels, names, action emphasis
- **Georgia / Times** — editorial/narrative cutaway copy
- **Playfair Display / serif** — Gazette/newspaper treatment

New UI should reuse this hierarchy.

Do not introduce unrelated display fonts into minigames.

## 5. Dashboard geometry

The dashboard is measured against `frame.webp`.

Important production coordinates:

- logo gap: y 83–155
- Season / Week / Record card: y 155–211
- economy card: y 227–315
- Sandra portrait opening: x 39–811, y 334–822
- notepad: approximately y 829–1488
- footer action cards: approximately y 1503–1655

The portrait window is **772 × 488** and uses a deliberate crop.

Any frame replacement must be re-measured before CSS coordinates are changed.

Do not "eyeball" dashboard alignment.

## 6. Character cards

The first-appearance/file-photo card displays a portrait at **384 × 448**.

Current legacy cast PNGs are only **96 × 112** and are enlarged with `image-rendering: pixelated`.

Until those portraits are deliberately rebuilt, treat that coarse file-photo look as a legacy visual treatment — not as the resolution target for new character art.

New character masters should be created at useful working resolution and reduced into the game deliberately.

## 7. Sawdust Sam

Sam must remain recognizably the same mascot across every scene.

Locked traits:

- gray wolf mascot
- red/black lumberjack-style cap
- Lumberjacks uniform when performing as mascot
- no jersey number unless a story specifically requires one
- big painted mascot eyes
- default expression deadpan/neutral rather than a cartoon grin
- adult performer proportions inside the suit
- scale consistent with nearby adults/referees

Arena scenes:

- Sam should be near referee/player human scale unless the joke is specifically the oversized head
- the court must not shrink to make Sam look large
- no unexplained changes to jersey, cap, muzzle or eye design between frames

## 8. Arena rules

The Lumberjack Shack has two canonical views: the wide arena master and the behind-the-basket master listed above. All new arena art must depict the **same building**.

Before approving an arena image, verify:

- arena remains a modest mid-size semi-pro building, never NBA-scale
- exposed rafters, practical warm lamps, worn institutional walls and crowd scale match the canonical masters
- scoreboard remains simple and period-appropriate: score, HOME/VISITOR, clock and period; no giant video display
- no championship banners or invented historical achievements
- no city name or generated sponsor/lore signage
- centre circle is geometrically centred
- the **single half-court line runs sideline-to-sideline through the centre circle**
- there is **no longitudinal line running from one key/basket through centre court to the other**
- key/lane treatment reads as early-1980s semi-pro, not modern NBA
- three-point marking exists where required and reads correctly
- hoop/backboard belongs to the court, never the stands
- players have plausible basketball spacing and movement
- front-row crowd reaches the court edge without blocking the action
- no random timber clutter
- feet/legs are visible when the scene requires full-body action
- no centre-court logo unless a story explicitly requires one
- court perspective remains consistent across an animation and between matched camera angles

If a generated raster conflicts with the locked geometry in `ARENA_MASTER.md`, the geometry rules win.

Comedy comes after believable space.

## 9. Sandra environment continuity

Special portraits should only be active for their intended story scope.

Examples:

- home arena portrait → home-arena story/game-night use
- gas station portrait → gas-station beat only, then back to desk
- road portrait → road/travel beat only
- awards portrait → Awards Night
- Blizzard portrait → Blizzard story/game-night only

After the special beat, restore the appropriate office/default portrait.

## 10. Minigame visual rules

All minigames are different activities inside one product.

**Sam Tunnel Escape is the current benchmark** for overall polish and integration.

Shared rules:

- full-bleed inside the host iframe
- `#14110f` or visually compatible dark base
- Courier New / game-approved type only
- no redundant standalone game title at the top when the host already supplied context
- UI should feel printed/painted/physical, not modern mobile-game chrome
- strong hierarchy: objective → status → action
- readable on iPhone at actual size
- result transition should return cleanly to the host game

Preserve each minigame's specific identity:

- Possum Fuse Box: Sierra/LucasArts electrical-room adventure feel
- Hotdish: clean, cared-for 1984 kitchen with correct food/object scale
- Sam Tunnel: dark escape-maze tension, current UI benchmark

## 11. Newspaper / institutional voice

Gazette visuals should feel like an actual small regional newspaper, not a parody prop.

- NORTH COUNTRY dateline
- institutional presentation
- restrained headline typography
- paper texture remains secondary to legibility
- no city name anywhere

## 12. Art-generation checklist

Before accepting a generated asset:

1. Is it authored for the exact production frame?
2. Does it look like the same game as the reference assets above?
3. Are character faces/models continuous?
4. Are adult characters visibly adult?
5. Is the physical space believable?
6. Is the joke readable without explanatory text?
7. Are there accidental signs, logos or readable nonsense?
8. Does it survive being viewed at actual iPhone size?
9. Does it preserve the unnamed-city rule?
10. Does its filename and code usage match the intended story scope?

## 13. Current known visual debt

Tracked in GitHub issue **Season 1 visual master pass**.

Highest-priority gaps include:

- missing Sandra Blizzard portrait
- missing renovated-office frame
- missing splash still fallback
- outdated Cheese/referee art
- 9:16 cutscene masters being cropped into 853 × 1844
- declared but absent story scenes
- legacy low-resolution cast portraits
- unused/duplicate portrait assets

Fix visual debt by improving the master asset or the integration — not by adding one-off CSS hacks around it.
