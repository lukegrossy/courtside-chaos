# Season 1 release checklist

Use this before merging a release candidate to `main`.

## Boot and save

- [ ] Fresh START reaches the opening sequence without a blank screen.
- [ ] A valid save exposes CONTINUE.
- [ ] CONTINUE restores the expected week, record, cash, morale, buzz and cred.
- [ ] START still begins a genuinely fresh game.

## Schedule and story continuity

- [ ] Week 1 is Tiny Open Mic / Day One.
- [ ] Week 2 is Possum Fuse Box.
- [ ] Regular season contains exactly 18 weeks.
- [ ] Sandra's leave announcement is followed by Grace the next week.
- [ ] Triggered stories do not create Week 19.
- [ ] The city is never named anywhere in player-facing copy.

## Minigames

- [ ] Possum Fuse Box opens full-screen and returns a result.
- [ ] Hotdish Night opens full-screen and returns the correct distinct result branch.
- [ ] Sam Tunnel Escape opens full-screen and returns the correct result.
- [ ] Stale minigame messages cannot resolve a later minigame session.
- [ ] Returning from a minigame restores the correct dashboard/portrait.

## Media and audio

- [ ] Home and road tip-off media load without obvious blank-frame delay.
- [ ] Blizzard cutscene and blizzard audio play in the intended story/game-night scope only.
- [ ] Sandra road, home-arena, awards and other special portraits return to the correct default afterward.
- [ ] Office ambience starts only after user interaction where required by iOS.
- [ ] No late-decoding audio starts underneath a later scene.

## Season ending

- [ ] Timber Cup Final sequence completes correctly.
- [ ] Postponed Ernie retirement resolves after the Final when applicable.
- [ ] Estate sequence acknowledges the earlier Arena Condemned choice.
- [ ] Awards Night completes with the locked outcomes.
- [ ] Final button says SEASON COMPLETE, not SEASON 2.
- [ ] Season 1 terminal completion state is stable on save/resume.

## iPhone Safari

- [ ] Portrait layout fits without horizontal scrolling.
- [ ] Tap targets are comfortably usable.
- [ ] Minigames remain full-bleed.
- [ ] Video plays inline rather than forcing the native full-screen player.
- [ ] Audio unlock works after a normal user tap.
- [ ] Home-screen web-app cache is not serving an older build after deployment.

## Deployment

- [ ] GitHub Actions quality gate passes.
- [ ] Merge to `main`.
- [ ] GitHub Pages deploy completes.
- [ ] Production URL is opened in a fresh Safari tab.
- [ ] Production URL is tested from the installed home-screen version.
