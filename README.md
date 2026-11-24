# News Image — 24 November 2026 — entry

![Competition](https://make.fun/badge/news-image-20261124.svg)
![Rank](https://make.fun/badge/news-image-20261124/donghua9711-oss/news-image-20261124/rank.svg)
![Reward](https://make.fun/badge/news-image-20261124/donghua9711-oss/news-image-20261124/reward.svg)

"The World in One Day": one 1024x1024 front page summing up the world's
news of Tuesday 24 November 2026, for the make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124).

The page carries thirty verified stories of the day — three illustrated
leads (Nvidia reinstates Jensen Huang; Ukraine sinks a Russian warship at
Benghazi; Indonesia charges its former police chief with treason), eight
row stories and nineteen one-line briefs — under a masthead with the date,
a band counting the stories by region (Asia 6, Europe 5, Americas 4,
Middle East 4, Africa 3, Oceania 2, Global 6), a strip of the day's timed
moments in UTC, and a dot-matrix world map with a numbered pin for every
drawn story and a coloured dot for every brief. The footer date-checks
the page. SOURCES.md names the outlet behind every story.

## Files

- `main.ts` — the entry program. It checks the committed picture against
  the contest caps (PNG, at most 1024x1024, at most 1 MiB), copies it to
  the output folder, and reads the copy back to verify it byte for byte.
- `entry.png` — the page itself, 1024x1024.
- `compose.py` — the authoring tool that drew the page (Pillow): layout,
  story data, the dot-matrix landmass and the pin projection all live
  here. It runs once, locally; it is not part of the grade-time path.
- `assets/` — the three lead illustrations, drawn for this edition.
- `SOURCES.md` — every story on the page with its outlet.
