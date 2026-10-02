# Courtside Chaos

Story-first basketball management game set in 1984.

You inherit **THE LUMBERJACKS**, a minor-league basketball club in the North Country, and survive one season through weekly owner decisions, game-night chaos, minigames, and Sandra's increasingly dry paperwork.

## Production

- **Platform:** single-file HTML/JS game with separate HTML minigames
- **Primary target:** iPhone Safari / installed web app
- **Hosting:** GitHub Pages
- **Default branch:** `main`
- **Development flow:** changes should go through a branch + pull request before merging to `main`

## Repository layout

- `index.html` — main game
- `assets/` — cutscenes, portraits, sound and UI artwork
- `minigames/` — full-screen iframe minigames
- `.github/workflows/` — automated release/canon checks

## Locked Season 1 invariants

These are release rules, not suggestions:

- Team name: **THE LUMBERJACKS**
- The city is never named
- Starting cash: **$40,000**
- Regular season: **18 weeks**
- Week 1: Tiny Open Mic / Day One
- Week 2: Possum Fuse Box
- CONTINUE must remain available for valid saves
- Season 1 ends after the Estate + Awards Night completion sequence
- No playable **SEASON 2** button in the Season 1 release
- Later-season plumbing may remain dormant in code

The automated quality gate protects a subset of these rules so accidental regressions are caught before merge.

## Local testing

Serve the repository over HTTP rather than opening `index.html` directly:

```bash
python3 -m http.server 8000
```

Then open:

```
http://localhost:8000/
```

For release testing, always include real iPhone Safari testing because audio, media loading, localStorage and home-screen web-app caching behave differently from desktop browsers.

## Release process

1. Create a branch from `main`.
2. Make one focused change.
3. Open a pull request.
4. Let the automated quality gate pass.
5. Run the manual checks in `RELEASE_CHECKLIST.md`.
6. Merge to `main`.
7. Verify GitHub Pages on iPhone Safari.

## Current release focus

Finish and polish **Season 1**. Preserve Season 2 plumbing only where it does not surface to players.
