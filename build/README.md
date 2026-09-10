# build

Regenerates the table tennis case study from the raw bet log. Two steps, no
dependencies beyond the standard library.

## Why there is a build step at all

The charts are inline SVG generated here, at build time, rather than drawn by a
chart library in the browser. That keeps the published page dependency-free and
lets the charts inherit the Tangerine chart tokens directly (see §9 of
`../CLAUDE.md`). The cost is that changing a chart means re-running a script
rather than editing markup.

## Running it

The raw log lives in a separate repo and is not vendored here:

```bash
gh repo clone tomfothergill/tabletennis
python build/build_stats.py tabletennis/Model_Assessment.csv
python build/render_page.py
```

`build_stats.py` reads the log and writes:

- `build/stats.json` — headline figures, the monthly series, the daily
  cumulative series, and the league and price-band breakdowns. Committed, so
  `render_page.py` works without the raw log.
- `../table-tennis/bets.json` — the compact match log the page loads on request.

`render_page.py` reads `stats.json` and writes `../table-tennis/index.html`.

Both are idempotent: re-running against the same log reproduces all three files
byte for byte.

## Editing the prose

Edit `article.html` for the article body, or the `HTML` template in
`render_page.py` for page metadata and the bet-log section. Then run
`python build/render_page.py`. The renderer overwrites `table-tennis/index.html`,
so direct edits to that generated page will be lost.

The period comparison reads `table-tennis/bets.json` to avoid adding rounded
monthly profits. Other figures use `stats.json`. Both inputs are committed.

The approved version before the full rewrite is at `table-tennis/baseline.html`,
with its original styles and generator saved in `build/baselines/table-tennis/`.

## Two things worth knowing

**Returns are exported at three decimals, not two.** 406 rows carry
three-decimal prices (2.625, 4.333). Rounding returns to two decimals made the
page's own recomputed total read +1220.53 against a headline of +1221.74 — and
the page's argument is that its arithmetic can be checked, so the two have to
agree exactly.

**The dormant-span annotation finds its own gap.** There are two breaks longer
than 45 days in the series: 59 days in mid-2022 and 283 days from December 2022
to October 2023. Both are drawn as dashes; the annotation attaches to whichever
is longest and derives the duration from the data, because hard-coding it
labelled the wrong gap.
