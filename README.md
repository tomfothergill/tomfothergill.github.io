# tomfothergill.github.io

My personal site. Plain HTML and CSS — no build step, no dependencies. Built on the **Tangerine**
design system; the rules live in [CLAUDE.md](CLAUDE.md).

Live at <https://tomfothergill.github.io>.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page. Content lives here. |
| `styles.css` | Tangerine tokens at the top, then one numbered block per band. |
| `CLAUDE.md` | The Tangerine design system in full. Read it before changing anything visual. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is instead of running them through Jekyll. |

## Editing

Edit `index.html`, commit, push to `main`. GitHub Pages redeploys within a minute or so.

To preview locally, open `index.html` in a browser, or serve it:

```bash
python -m http.server 8000
```

## Custom domain

Add a `CNAME` file containing the bare domain (e.g. `example.com`), point a
`CNAME` DNS record at `tomfothergill.github.io`, then enable "Enforce HTTPS"
in the repo's Pages settings.
