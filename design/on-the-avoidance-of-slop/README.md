# On the avoidance of slop

Approved article copy is in `article.md`, including the final paragraph revisions.
Run `python design/on-the-avoidance-of-slop/build.py` from the repository root
to reproduce the HTML, individual cut-outs and two decorative SVG sequences.
The build uses Pillow, NumPy and SciPy; the published page needs no JavaScript.

Source: the user's `egyptian-3-1600.jpg` download, retained unchanged in
`assets/patterns/egyptian/egyptian-3.jpg`.
[Egyptian Capitals](https://www.oldbookillustrations.com/illustrations/egyptian-3/),
Egyptian No. 3, plate VI, from Owen Jones's *The Grammar of Ornament*, 1868 edition.
Lithographer: Francis Bedford; artist unidentified in the catalogue.

Eight individual specimens are isolated using loose polygon bounds and an
exterior paper flood mask. Enclosed illustration colours and paper texture
are retained. Different sequences run down each margin, with generous space
between figures. SVGs embed the PNGs so CSS backgrounds have no external image
dependencies. The cream, dark ink, green links and terracotta labels draw from
the plate; typography and reading layout follow the other articles.

The borders disappear at 900px and below, where whole specimens would be too
narrow to read. Thomas selected the smaller columns for deployment, at 64% of the original
width and height, centred in each original position. Production uses
`left-small.svg` and `right-small.svg`. The homepage includes the new article as IV.

Checked the cut-outs visually, the desktop article at 1440px, and tablet/mobile
layouts at 1000px and 390px. No horizontal overflow; all 20 approved paragraphs
are present. `git diff --check` passes.

## Border comparisons

Run `python design/on-the-avoidance-of-slop/build-previews.py` to rebuild two
independent pages in `design/slop-preview/`. The original article is untouched.
`smaller-columns.html` reduces each Egyptian specimen to 64% of its original
width and height while keeping its position in the sequence.
`italian-pattern.html` uses the bottom-left vertical panel from the user's
`italian-2-1600.jpg`, cropped to (51, 617, 212, 1542) without its frame, and
blended with the cream page ground. Each preview links to both alternatives
and the original. Both retain all 20 paragraphs and were checked at desktop
and 390px mobile widths, with no horizontal overflow.
