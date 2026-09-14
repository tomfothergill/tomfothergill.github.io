# Articles as found documents

Implemented from `Article Layout Spec.dc.html` in the 14 September 2026 Claude
Design bundle `Tangerine article decoration concepts-handoff.zip`. This is the
primary specification; the other concept sheets are earlier explorations.
The homepage is explicitly outside this design's scope.

## Layout

- Article-only stylesheet: [article-layout.css](../../article-layout.css), loaded
  after the existing styles. The homepage's HTML and styles are unchanged.
- Cormorant Garamond headings, Newsreader prose, DM Mono metadata.
- Centred 700px column with 48px internal gutters (604px reading measure),
  19px/1.65 body text, 24px between paragraphs.
- Patterns run along the article body only, with no decoration behind the text.
  Strips are 180px wide, 96px below 1100px, 40px below 900px and hidden below
  700px. Mobile uses 22px page gutters and 18px prose.
- Figures step out 50px per side, reduced to 30px at tablet sizes and zero on
  mobile. Tables, detailed diagrams and mobile charts scroll within their own
  containers so the page never scrolls horizontally.
- Header and footer sit on the article ground; the former contact band and
  table-tennis opener illustration are removed. Pattern credits close each page.

## Article themes and assets

| Article | Pattern | Ground | Body | Labels | Links |
| --- | --- | --- | --- | --- | --- |
| Frontend | Kiosk tiles, Prisse d'Avennes, 1877 | `#F2EBD5` | `#23222B` | `#B93E29` | `#4C5A82` |
| Analytics agent | Study of Leaves and Fleurons, Émile Prisse d’Avennes, 1877 | `#FAFCF1` | `#203D41` | `#386648` | `#245F80` |
| Table tennis | Floral scrollwork, Owen Jones, 1867 (adapted) | `#F4EEE3` | `#4A1C24` | `#3D7848` | `#4A1C24` |

The kiosk label red and chintz label green are slightly darker than the handoff's
`#C6432C` and `#3F7A4A` to meet its 4.5:1 label contrast requirement. Prose contrast
is at least 11:1 for all three themes.

The kiosk and chintz PNG crops in [assets/patterns](../../assets/patterns/) are
copied unchanged from the supplied handoff, with its attribution retained.
Their background tile widths are 416px and 400px. The analytics pattern was
subsequently replaced with the user-supplied Leaves and Fleurons scan described
below. These remain the supplied image resolutions; no high-resolution
replacement scans have been substituted. A verified public-domain source for the
chintz plate is [Rawpixel's original plate](https://www.rawpixel.com/image/329518/free-illustration-image-flower-vintage-sir-matthew-digby-wyatt).

## Maintaining the pages

- Table tennis is generated: edit [build/article.html](../../build/article.html)
  and [build/render_page.py](../../build/render_page.py), then run
  `python build/render_page.py`. The generator retains the full log, filters,
  pagination, chart interaction and data. It reproduces the generated page.
- The other two pages are static HTML. Preserve their complete article copy and
  link targets. The frontend article's old colour-scheme aside was removed at
  Thomas's request when applying this redesign.
- Both architecture diagrams retain their geometry and labels. Their standalone
  SVGs match the inline diagrams' new palette.
- The bundle's `support.js` is a Claude Design preview runtime, not a production
  dependency. It is not included in the site.

## Verification

Checked all three articles at 390, 768, 1000 and 1440px with no page overflow;
visually reviewed their desktop layouts, mobile table-tennis layout, diagrams
and log. Confirmed chart keyboard navigation and the full 10,382-row log's load
and result filtering. Confirmed the homepage and its existing shared CSS remain
byte-for-byte unchanged, and verified repeatable table-tennis generation.

## Analytics pattern replacement

Thomas replaced the Indian lac-work pattern with `leaves-fleurons.jpg` from
Downloads. The original 500 × 712 JPEG is retained unchanged. The SVG field
asset embeds that JPEG in a cropped viewport (`23 23 454 636`) to keep the plate
caption and outer mat out of the repeating strip; it is displayed at 416px wide.
The page now uses the scan's pale ground, dark blue-green ink, green labels and
blue links. Both architecture diagrams use the same palette.

Credit: [Study of Leaves and Fleurons](https://www.oldbookillustrations.com/illustrations/leaves-fleurons/),
Émile Prisse d'Avennes, *L'art arabe*, 1877, plate 130.

## Table tennis pattern replacement

The user replaced the red chintz pattern on the table tennis article with `from-you-headpiece-1600.jpg`.
The original 1600 × 600 JPEG is stored unchanged as `from-you-headpiece.jpg`.
An SVG viewport presents the ornament vertically, with its outer whitespace
cropped, repeated at the current strip width. CSS multiply blending matches the
scan's white paper to the existing cream ground. Typography, article copy and
responsive strip visibility remain unchanged.

Credit: [Two-Color Headpiece with Circular Pattern](https://www.oldbookillustrations.com/illustrations/from-you-headpiece/),
John Sliegh, *Odes and sonnets, illustrated*, 1866. The homepage credit also
reflects this replacement.

## Selected cream floral vine

The table tennis page now uses the upper panel of `china-vase-2-1600.jpg`,
rotated into a vertical border. The pale blue areas were selectively recoloured
to the article cream, retaining the scan texture and full-strength flowers and
vines. The heavy navy framing bands are removed: the final 492 × 1568 PNG
crops x=80..572 from the rotated cream preview. It repeats at the strip width
without multiply blending. The page background and mobile visibility are unchanged.

Source: [Borders with Scrolls and Floral Design](https://www.oldbookillustrations.com/illustrations/china-vase-2/),
Owen Jones, *Examples of Chinese ornament*, 1867. The page credit marks it adapted.
Earlier alternatives in `design/pattern-preview/` are local comparison pages.

## Article headers: 2B centred title page

Selected from `Article Top Options.dc.html` in `Article header.zip` on 14 September 2026. All four articles use a full-width centred opener, 92px desktop title limited to 16ch, centred 44ch standfirst, and a full-width rule above the patterned article body. Desktop padding is 76px 56px 64px with 30px gaps. Titles scale down on narrower screens; mobile retains 22px gutters. The table-tennis opener no longer repeats the statistics shown immediately below. Article prose, patterns and homepage are unchanged.
