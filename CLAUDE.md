# CLAUDE.md

This repo is Thomas Fothergill's personal site: plain HTML and CSS, no build step,
no dependencies, served from GitHub Pages at <https://tomfothergill.github.io>.

Every visual decision in this repo follows the **Tangerine** design system below.
It is not a suggestion. If a change would break one of these rules, say so and
propose an alternative that stays inside the system rather than bending it.

Source: `Tangerine Design System.dc.html`, Claude Design project
`15c59770-204c-4cd6-b4fb-caab07df9225` (design system 01, September 2026,
derived from option 4A in *Theme Explorations*).

---

## 1. The idea

The site should feel like a break from the rest of the internet. Tangerine does
that by refusing the default: no white page, no card grid, no cookie banner, no
newsletter. A visitor lands on a field of orange with one sentence on it, set at
88px in a serif drawn for headlines.

Three rules hold it together:

1. **Colour is a ground, not an accent.** Orange covers the page; the ink sits on top of it.
2. **Type carries the hierarchy.** No decorative rules, icons or illustrations doing that job.
3. **The page tells the truth about itself.** The footer says there is no newsletter, and there isn't one.

It is warm and slightly odd, which is the point. Aubergine on hot orange is not a
corporate pairing, and an engineering portfolio that looks like a risograph poster
is remembered.

## 2. Colour

Four values in a fixed proportion. Tangerine is the page. Aubergine is every piece
of type on it, plus the two inverted bands. Cream appears only inside aubergine.
Amber is for secondary type inside aubergine and nowhere else.

| Token | Hex | Used for | Share |
| --- | --- | --- | --- |
| `--field` | `#FF7A1A` | Page ground; hover-state text on aubergine | ~70% |
| `--ink` | `#330A37` | All type on the field; band and footer grounds | ~22% |
| `--cream` | `#FFE9CC` | Type on aubergine; hover-row text | ~5% |
| `--amber` | `#FFB86B` | Secondary type on aubergine only | ~2% |
| `--ink-soft` | `#5C1A62` | Eyebrow labels and secondary type on the field | ~1% |
| `--note` | `#C0392B` | Footnote markers and links in prose only | <1% |

**Contrast, computed sRGB.** Ink on field 6.5:1. Cream on ink 14.4:1. Amber on ink
9.9:1, and capped at 11px caps regardless. Ink-soft on field is 4.53:1 — it clears
the 4.5 floor by three hundredths, so use it for **uppercase labels only, never for
paragraphs**, and re-measure if `--field` is ever adjusted.

**Rules of use.** Never tint the field: no gradients, no orange-on-orange panels, no
opacity layers over it. Hairlines on the field are `rgba(51,10,55,0.3)`; structural
rules are solid ink at 1.5px. A hover state does not lighten or darken anything — it
swaps ground and ink outright, field-to-aubergine.

**The inversion, in full:** aubergine grounds get cream type, amber metadata, and
tangerine only for a link or an arrow.

**Article pages are inverted.** The home page is tangerine; article pages carry
`class="inverse"` on `<body>` and go aubergine: cream type, amber labels and
metadata, tangerine prose links (`--note` is 2.4:1 on aubergine and unusable
there), hairlines at `rgba(255,233,204,0.22)`, and the bands and footer invert
back to tangerine with ink type so they still read as bands. This is §2's
inversion rule applied page-wide, not a new palette: ink on tangerine is 6.5:1
and fine for 45 words; cream on aubergine is 14.4:1 and is the long-read
surface. Cover orange, pages aubergine.

In CSS the colour tokens (`--field`, `--ink`, …) never change. Six role tokens
sit on top — `--ground`, `--type`, `--type-soft`, `--link`, `--rule`, and the
`--inverse-*` set for bands and footer — and `.inverse` remaps them once. Style
with roles, never with colours directly.

There is no dark mode. The palette is the design; do not add a
`prefers-color-scheme` variant.

## 3. Typography

Two faces do the work, with a third reserved for long reading. **Instrument Serif**
is the voice: display sizes only, never below 20px. **IBM Plex Mono** handles
everything structural — navigation, eyebrows, dates, tags, footers — always
uppercase with wide tracking at small sizes. **Newsreader** is added for case-study
prose, where mono would be unkind past a paragraph.

| Role | Face | Size / line | Notes |
| --- | --- | --- | --- |
| Statement | Instrument Serif | 88 / 0.94 | 17ch measure, −0.02em, one per page |
| Page title | Instrument Serif | 52 / 1.02 | Case-study openers, 24ch measure |
| Row title | Instrument Serif | 36 / 1.1 | Work index rows |
| Section lede | Instrument Serif | 24 / 1.35 | About block; note titles at 20 |
| Body / prose | Newsreader 400 | 17 / 1.7 | Max 46ch on field, 62ch on cream. Was 300; too light to read at length |
| UI body | IBM Plex Mono | 13 / 1.9 | Home supporting text; row summaries at 12 |
| Eyebrow / meta | IBM Plex Mono | 10 / 2.0 | Uppercase, 0.20–0.22em tracking |

Never set Instrument Serif below 20px, never set Plex Mono above 13px, and never
track uppercase mono below 0.16em. Numerals in metadata use the mono face so dates
and years align down a column.

## 4. Layout

One column, full-bleed, 40px page gutters. Content is **not** centred in a
container — it runs edge to edge and is held by the gutters, which is what makes the
colour feel like a ground rather than a box.

The page is a fixed sequence of six bands, top to bottom:

1. A 16px rule-bar of navigation
2. The statement block
3. A full-width metadata band in aubergine
4. The work index
5. A two-up about-and-notes grid
6. The contact footer in aubergine

Every page in the site is a subset of that sequence **in the same order**. A case
study replaces the statement with a 52px title and the work index with prose.

**Spacing scale — 4, 8, 12, 16, 22, 26, 34, 40, 44, 64.** Band padding is 44px
vertical, 40px horizontal. The statement block gets 64px above. Rows are 22px
vertical. Grid gaps are 40px. Nothing uses a value off this scale. (In CSS these
are `--s1`…`--s10`.)

Asymmetry is deliberate and always the same shape: supporting prose sits left at a
44ch measure, and location or status metadata sits right, uppercase mono,
baseline-aligned to it. Do not centre either.

## 5. Components

Six, and the system needs no more.

- **Rule-bar** — Name left, four links right, 10px uppercase mono, 1.5px ink rule beneath, 16px padding. Never sticky, never a burger menu; at four items it wraps to two lines on narrow screens.
- **Statement** — 88px serif at a 17-character measure so line breaks are authored, not accidental. Below it, the left prose / right metadata pair. One per page, always the first thing after the rule-bar.
- **Metadata band** — Full-bleed aubergine strip, 11px vertical padding, amber uppercase mono, 34px gaps. Holds the working vocabulary. Optionally a slow marquee that pauses on hover; **static is the default**.
- **Work row** — Number, 36px serif title, right-aligned discipline and year, and a 12px mono summary indented 58px to sit under the title. Hover inverts the whole row to aubergine with cream type. **Three rows maximum** on the home page.
- **Two-up grid** — Equal columns, 40px gap: about on the left as a single 24px serif paragraph with one underlined mono link; notes on the right as dated rows with hairline rules. Collapses to one column under 700px.
- **Contact footer** — Aubergine ground, the email address as 36px cream serif, three amber mono links right. The last link is always the disclaimer: "no newsletter".

There are no buttons in the ordinary sense. A call to action is either an underlined
mono label or a solid aubergine block with cream uppercase mono inside it, which
inverts to cream-on-ink on hover. **No radii anywhere: every corner is square.**

## 6. Motion and states

Motion is a response to the cursor, not an entrance animation. Nothing fades in on
scroll, nothing moves on load, and there is no page transition.

- **Hover** — 160ms ease-out on colour, full inversion, no intermediate tint.
- **Transform** — 420ms `cubic-bezier(.2,.8,.2,1)`.
- **Reveal** (blinds, panels) — 520ms `cubic-bezier(.65,0,.35,1)`, 34ms per-slat stagger.
- **Focus** — 2px ink outline, 2px offset.
- **Reduced motion** — all transforms become instant state changes; colour transitions stay.

One optional mechanic per page, maximum. The candidates are the marquee band, the
sequenced blinds on the work index, and cursor-magnetic letters on the statement.
Two at once makes the page restless and cancels the calm the colour is doing.

## 7. Imagery and iconography

There are no icons. Arrows are typed characters — `→` and `↓` in the mono face.
Bullets are numbers. Nothing in the interface is drawn.

**One drawing per case study** (from `Opener Illustration.dc.html`, placement
12A): a single-weight line drawing beside the headline, 260px wide, top-aligned
to the h1, in the space the 24ch headline leaves empty. It faces into the page.
The file is an alpha-only PNG and the line is filled from `--type` through a CSS
mask (`.opener__art`, with the page supplying the file via `--art`), so it is ink
on the cover and cream on an inverted page from one asset. Cream on aubergine
thickens optically: never below 200px there. Draw what the article is about,
not the sport in general; no stock line art, nothing generated — both read as
filler next to prose this specific. One per case study, not a set; the identity
stays the colour and the type.

Case studies carry real screenshots, diagrams and plots, placed full-bleed within
the gutters with a 1.5px ink border and a 10px mono caption beneath. Until real
assets exist, use a diagonal-stripe placeholder in cream and tangerine with a mono
label saying what belongs there. Do not use stock photography, and do not use
generated abstract imagery.

## 8. Voice

First person, past tense, specific numbers. Every project headline names the
surprising finding rather than the technology: "graders disagreed with each other
more than with the model" instead of "LLM evaluation framework". Sentence case in
prose, uppercase only in mono metadata. No exclamation marks, no emoji, no job-title
jargon, and no adjectives about yourself.

Admit limits in the copy, because that is what makes an engineering portfolio
credible: what the model got wrong, what you were not allowed to change, what you
would not ship. The footer's small refusals — no newsletter, no analytics — are part
of the voice, not decoration.

**Length:** a statement is under 12 words, a row summary under 20, an about
paragraph under 45.

## 9. Charts

Charts were the first thing to break the system, for a diagnosable reason: on the
field there is exactly one usable ink, so every mark is the same colour as every
other mark and value can only be encoded by position. That is enough for one
series and nothing more. The fix is not more hues on the field — it is moving
data onto a ground that has a value range in it.

### 9.1 Amendment to §4 — the data surface

Every chart sits on an aubergine panel. §4 forbids light panels on the field and
reserves aubergine for full-bleed bands; this amends the second half of that rule
rather than breaking it. Aubergine is legal as a contained ground when it is a
**data surface**, subject to three conditions: it spans the full content width
between the gutters, so it still reads as a band and not a card; it is
square-cornered with no border and no shadow; and it contains only marks, axes
and one readout — no prose, no headings, no buttons.

The only exception is a single-series sparkline: under 60px tall, drawn in ink
directly on the field, with no axes, gridlines or tick labels. If it needs a
label, it needs a panel.

Panel padding is 26px, or 34px when there is a readout slot. Eyebrow, chart title
and source note live **outside** the panel, in field colours, using the existing
type roles.

**The panel-to-field join: treatment 7A, full-bleed band.** "Full content width"
means the panel breaks out of the page gutters entirely and runs edge to edge —
an inset on all four sides makes it a card dropped on the page, which is the
thing this rule exists to prevent. The gutter becomes the panel's *inner*
horizontal padding instead, so chart content still lines up with the text column
above it. In CSS that is `margin-inline: calc(var(--gutter) * -1)` plus
`padding: var(--s7) var(--gutter)`.

Chosen from `Chart Panel Treatments.dc.html` over the hard-offset, hatched-shim,
notched and passe-partout alternatives. Its known weakness is that at wide
viewports the band can read as a hole punched in the page; if that becomes a
problem the fallback is 7B (a cream slab misregistered 8px down-right), not a
shadow. Explicitly refused: soft drop shadows, noise or paper grain, gradients
or inner glows on the panel, and rounded corners.

### 9.2 Tokens — extend, don't invent

The series ramp is the existing palette redeployed as ink on aubergine. Three of
the four series colours are tokens you already have; one hue is added, and it is
the only addition the chart layer is permitted. The system stops reading as
Tangerine the moment a second new hue appears — so the hard rule is **four series
maximum**, and if the data needs more, the chart is wrong and the answer is small
multiples.

| Token | Value | Role |
| --- | --- | --- |
| `--chart-ground` | `#330A37` (= `--ink`) | Panel ground. No other ground is legal. |
| `--series-1` | `#FFE9CC` (= `--cream`) | Primary series. Single-series charts use only this. |
| `--series-2` | `#FFB86B` (= `--amber`) | Comparison — prior period, forecast, benchmark. |
| `--series-3` | `#FF7A1A` (= `--field`) | Third series. The field colour becomes data ink here. |
| `--series-4` | `#C98FBF` **(new)** | Fourth and last. The one permitted addition. |
| `--chart-recede` | `#5C1A62` (= `--ink-soft`) | Unfocused marks during a focus state. |
| `--chart-grid` | `rgba(255,233,204,0.22)` **(new)** | Gridlines. The aubergine twin of the field hairline. |
| `--chart-hatch` | 45°, cream at 0.38, 1px on 5px | Negative-value fill. Not a colour — a texture. |

Series order is fixed: assign 1, then 2, then 3, then 4 — never pick by taste.
Contrast on `--chart-ground`: series-1 14.4:1, series-2 9.9:1, series-3 6.5:1,
series-4 6.6:1, recede 1.44:1 (intentionally illegible — it is context, not
content).

`--note` (`#C0392B`) stays out of charts entirely. It is the footnote marker, and
if it also meant "loss" then a link in a case-study paragraph would start looking
like a data statement.

### 9.3 Positive and negative

Sign is encoded by **fill, not hue**: positive is solid, negative is hollow — a
1px cream outline with the hatch texture inside. This survives greyscale
printing, survives every form of colour blindness, and keeps the series colour
free to mean *which series* rather than *which direction*.

Sign is always double-encoded. Negative marks hang below a 1.5px cream zero line
and their labels carry a minus. For lines, a negative or drawdown span switches
from solid to a 3px dash at the same colour and weight — the line never changes
colour mid-series.

### 9.4 Focus, not hover

The inversion rule in §6 governs interactive rows and blocks. It does **not**
apply to data marks, and applying it would be actively wrong — inverting a bar
swaps it with the panel and destroys the comparison the chart exists to make.

Charts get a focus state instead, and the distinction is that the subject is
never touched: on hover of a mark, every **other** mark drops to `--chart-recede`
at 160ms ease-out while the focused mark keeps its exact colour.

The value appears in a fixed readout slot in the panel's top-right — **never a
floating tooltip**, which would need a radius, a shadow and a light ground, all
forbidden. The slot is always present and shows the series total when nothing is
focused, so nothing shifts when it changes. Keyboard: arrow keys step focus along
the series, 2px cream outline at 2px offset. Under reduced motion the recede is
instant.

### 9.5 Axes, gridlines, labels

The existing weights carry over with one substitution. The 1.5px structural rule
becomes the zero line, in cream, and it is the only 1.5px stroke in a chart. The
field hairline does not carry over — it is defined against orange and vanishes on
aubergine, hence `--chart-grid`.

- **Zero line** — 1.5px `--series-1`, full width.
- **Gridlines** — 1px `--chart-grid`, horizontal only, four maximum.
- **Axis lines** — not drawn. The labels do that work.
- **Tick labels** — 10px Plex Mono uppercase, 0.16em, `--amber`, every third category at most.
- **Value annotation** — 11px Plex Mono cream with a 1px cream leader, one per chart, no arrowhead.
- **Axis titles** — none. Use the 10px eyebrow above the panel.

Legends are inline mono labels at the top of the panel with a 10px square swatch,
never a boxed key in a corner. One series means no legend at all.

Bar gaps are 4px at 24 categories and 8px at 12 or fewer; bars never carry a
radius or a gradient. Past about 40 categories the chart becomes a line.

A cumulative line is the one chart type where the zero line is load-bearing even
when nothing goes below it, because the whole claim is distance from zero.

### 9.6 Charts on inverted pages

On an article page the panel goes **tangerine with ink marks** — the chart
tokens are remapped under `.inverse`: ground = field, series-1 = ink, gridlines
and recede = the field hairline value, hatch = ink at 0.38. That means exactly
one usable series, because amber and cream have no contrast on orange. Both
current charts are single-series (the bars encode sign by fill), so nothing is
lost here; a future two-series comparison on an inverted page needs small
multiples, or a decision to reopen this section. Do not put an aubergine panel on
an aubergine page — it has no edge without a border or shadow.

### 9.7 The inherited pattern

Aubergine panel, series assigned in fixed order, sign by fill, context receding
rather than subject changing, and one readout in a fixed slot. A scatter, a
histogram or a small-multiple grid needs no new decisions. A chart type that
genuinely cannot be expressed this way is the signal to come back to this
section, not to add a colour.

## 10. Tables

Tables go on the field, not on a panel — the opposite of charts, for the opposite
reason. A chart needs a value range to separate marks; a table separates its
content by position and alignment, so one ink is all it ever needed. Ink on
tangerine at 6.5:1 is a good reading surface for figures, and the flatness that
ruins a chart is exactly right here.

The one exception: a table that exists to itemise a chart directly above it moves
onto the same aubergine panel and adopts the chart tokens, so the pair reads as
one object. Never split a table and its chart across two grounds.

## 11. Article layout

Case-study prose takes **two-thirds of the content width**, and the **margin
column** — figures, definitions, sources, scoreboards — takes the final third, so
the page fills a laptop screen rather than leaving the right side empty. The
prose size is fluid, 17px at 1000px wide rising to 22px from 1440px, so the line
stays near 70–80 characters as the column widens instead of running to 100.
Margin items are capped at 36ch so a label/value row does not stretch across the
whole third. (The artboards in `Article Layout Ideas.dc.html` drew fixed 46ch and
26ch columns; Thomas asked for the fill, 2026-09-09.) Treatments 9A, 9B and 9D.
In CSS: `.article`, `.row2`, `.row2__margin`.

**The margin (9A).** Each row of the article is a grid: prose left, margin right.
The margin's hairline runs the whole length of every row whether or not there is
anything in it, so the column reads as structure rather than as floating boxes;
an empty margin is fine and most rows should have one. Rows are separated by the
same hairline used between work rows. Aim for roughly one margin item per two
paragraphs — more and it competes with the prose. Items are a 10px mono eyebrow
label and then either label/value rows with hairline rules, plain 11px mono
lines, or an 11px ink-soft note. Instrument Serif is not used in the margin
below 20px.

**When a chart or table arrives (9B).** It breaks out to the full content width
exactly as §9 builds it; the margin simply stops for its height and resumes
underneath. The caption moves into the margin of the next row, labelled "Above",
and that row carries no hairline above it, so the figure sits tight against the
prose on both sides. Figures inside the article carry no vertical margin of their
own — the rows do that work.

**The scoreboard (9D).** At story points the same margin column holds the
figures as they stood then: a 1.5px ink rule opens the rail, an "As of" eyebrow,
the cumulative figure at 52px in the serif (it has no dark ground to carry it, so
it goes up a size), a 10px mono sub-label, three or four hairline rows with
ink-soft labels, and a single-series sparkline under 30px. The month the reader
is at keeps its ink; the rest recede to the hairline value, which is the chart
focus rule reused. This is the *no-card* version — the aubergine-card scoreboard
was rejected because §9.1 reserves aubergine for full-width data surfaces. It
does not scroll or swap; it is placed statically where the story reaches that
moment.

**Values snapped to the spacing scale.** The artboards used 36px row padding,
56px column gap and 24px rail inset; the build uses 34, 44 and 26 so nothing is
off-scale. Below 700px the margin collapses beneath the prose and empty margins
disappear.

## 12. Don't

- Put a white or cream panel on the field to hold body text. Type goes directly on the orange.
- Introduce a fifth colour, a gradient, a drop shadow, or a rounded corner.
- Set the serif in uppercase, or the mono in sentence case at small sizes.
- Add a hero image behind the statement. The colour is the hero image.
- Use opacity to make a secondary colour. Use `--ink-soft` or `--amber`, which are real tokens.
- Add a fourth project to the home page. The index is deliberately three deep.
- Draw a chart on the field with more than one series, or on any ground other than aubergine.
- Encode gain and loss by hue, or bring `--note` into a chart.
- Invert a data mark on hover, or replace the readout slot with a floating tooltip.

---

## Working in this repo

- `index.html` — the home page, one section per band in the order above.
- `styles.css` — tokens first, then one numbered block per band. Comments cite the rules.
- `case.css` — case-study additions: the 52px opener, the chart layer (§9), the article grid and margin (§11), tables, and the filterable log.
- `table-tennis/` — case study 01. **Generated** — see below.
- `build/` — the generators for the table tennis page, plus their README.
- `.nojekyll` — tells GitHub Pages to serve the files as-is rather than running Jekyll.

`table-tennis/index.html` is written by `build/render_page.py` and its charts are
SVG generated at build time, so the page needs no chart library. Do not edit that
file directly — edit the template inside `render_page.py` and re-render, or your
changes are overwritten. `build/README.md` has the commands.

No build step and no dependencies. Fonts come from Google Fonts; everything else is
local. Edit, commit, push to `main`, and Pages redeploys within about a minute.

Preview locally with `python -m http.server 8000`, and **verify meaningful visual
changes in a browser before calling them done** — a successful load is not proof the
layout is right.

Commits in this repo use the GitHub noreply address
(`74731740+tomfothergill@users.noreply.github.com`) so the work email stays out of
public history. `gh` has two accounts configured; personal work here needs
`gh auth switch --user tomfothergill`.
