# tomfothergill.github.io

My personal site. Plain HTML and CSS — no build step, no dependencies.

Live at <https://tomfothergill.github.io>.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page. Content lives here. |
| `styles.css` | Design tokens at the top, then layout and type. Light and dark themes both defined. |
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
