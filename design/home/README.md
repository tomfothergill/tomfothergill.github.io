# Homepage: Endpaper

Thomas selected Round 11B from `Front Page Round 11.dc.html` in the
14 September 2026 Downloads bundle `front page.zip`.

The homepage uses `home.css` independently of the article styles. The original
placeholder copy, article summaries and real navigation targets are retained.

- Iris border (Hervégh, plate 3), copied unchanged from the handoff to
  `assets/patterns/iris-border.png`, repeats at 200px wide over a navy ground.
- Cream `#F4EEE3` bookplate, 860px wide including padding, with a 1px border and
  inset rule; 96px space above and below on desktop.
- Cormorant Garamond headings, Newsreader prose and DM Mono labels. Ink is
  `#1F1B17`, secondary text `#6B655C`.
- Roman numerals and pattern credits connect the work list with the articles.
  The analytics credit reflects the later Leaves and Fleurons replacement.
- Below 900px, metadata moves beneath each summary. Below 600px, the page uses
  narrower gutters, a stacked header and single-column About/Notes sections.
- The prototype runtime `support.js` is not a production dependency.

Article pages and shared article styles are independent of this homepage change.

Verified the desktop and mobile layouts visually, including the footer, and
checked 320, 390, 768, 1200 and 1440px widths for page overflow. All local links
and assets resolve. Article HTML and shared CSS hashes are unchanged.

## Floral vine replacement

The user replaced the iris surround with the central floral band from
`china-bottle-1-1600.jpg`. The original scan is retained unchanged at
`assets/patterns/china-bottle.jpg`. `china-floral-vine.svg` embeds it in a
cropped viewport (`14 208 1570 592`), excluding the upper scrollwork and lower
striped and ornamental borders. It repeats at 800px wide and blends with the
cream background. The bookplate, typography and mobile layout stay the same.
