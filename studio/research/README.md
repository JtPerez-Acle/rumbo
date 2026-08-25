# Research source material for courses

Drop a course's deep-research results here as a markdown/text file, then point the
course's `channels/<slug>.toml` at it with `research_file = "<name>.md"`.

The course factory injects this text into both syllabus and lesson generation as
**authoritative source material** — lessons must reflect the real features, steps,
and best practices in the research, not the model's own (possibly stale) knowledge.
This matters most for fast-changing topics like ad platforms.

Expected files (fill with your deep research, then run the factory):
- `meta-ads.md`
- `tiktok-ads.md`
- `facebook-ads.md`   (only if kept separate from Meta Ads — see note below)

## Note on Meta Ads vs Facebook Ads
"Meta Ads" (Meta Ads Manager) already covers Facebook **and** Instagram placements,
so a separate "Facebook Ads" course overlaps ~70-80%. Decide before generating:
either one "Meta Ads" course (recommended) or a Facebook-specific angle that
deliberately avoids duplicating the Meta course.
