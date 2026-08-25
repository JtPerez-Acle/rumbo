# Launch video

`brag.mp4` — 20s, 1920x1080. Built with [/brag](https://github.com/latent-spaces/brag)
on this repository, composed and rendered with
[Hyperframes](https://hyperframes.heygen.com/).

- `brag-plan.md` — the creative plan: angle, hook, storyboard, honesty constraints
- `composition-brief.md` — the brief handed to Hyperframes
- `composition/` — the composition source (HTML + GSAP timeline)
- `share-copy.txt` — the caption

## Re-rendering

The music bed and SFX are **not committed**. They ship with the `/brag` plugin and
its own README asks that redistribution terms be verified before republishing, so
this repository does not carry them. The rendered `brag.mp4` embeds them under
ordinary use of a bundled asset.

To re-render, restore the three files the composition expects:

```
composition/assets/audio/music.mp3   <- happy-beats-business-moves-vol-1-by-ende-dot-app.mp3
composition/assets/audio/click.ogg   <- sfx/ui/click2.ogg
composition/assets/audio/paper.ogg   <- sfx/interface/drop_001.ogg
```

all from `~/.claude/plugins/cache/brag/<version>/skills/brag/assets/`, then:

```bash
cd composition && npx hyperframes check && npx hyperframes render -o ../brag.mp4 -q high
```

Requires Node 22+ and ffmpeg on PATH.
