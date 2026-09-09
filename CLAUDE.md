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
| Body / prose | Newsreader 300 | 17 / 1.7 | Max 46ch on field, 62ch on cream |
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

## 9. Don't

- Put a white or cream panel on the field to hold body text. Type goes directly on the orange.
- Introduce a fifth colour, a gradient, a drop shadow, or a rounded corner.
- Set the serif in uppercase, or the mono in sentence case at small sizes.
- Add a hero image behind the statement. The colour is the hero image.
- Use opacity to make a secondary colour. Use `--ink-soft` or `--amber`, which are real tokens.
- Add a fourth project to the home page. The index is deliberately three deep.

---

## Working in this repo

- `index.html` — the home page, one section per band in the order above.
- `styles.css` — tokens first, then one numbered block per band. Comments cite the rules.
- `.nojekyll` — tells GitHub Pages to serve the files as-is rather than running Jekyll.

No build step and no dependencies. Fonts come from Google Fonts; everything else is
local. Edit, commit, push to `main`, and Pages redeploys within about a minute.

Preview locally with `python -m http.server 8000`, and **verify meaningful visual
changes in a browser before calling them done** — a successful load is not proof the
layout is right.

Commits in this repo use the GitHub noreply address
(`74731740+tomfothergill@users.noreply.github.com`) so the work email stays out of
public history. `gh` has two accounts configured; personal work here needs
`gh auth switch --user tomfothergill`.
