# Analytics agent — design handoff

- [Article copy](article.md): the draft used for the published article.
- [Architecture diagrams](architecture-diagrams.md): editable Mermaid diagrams, captions and design notes for the earlier multi-agent orchestration and current single-agent loop.
- [Published page source](../../analytics-agent/index.html): the live article's HTML.
- [Article styles](../../analytics-agent/article.css): additions to the shared site styles.

The article is live at <https://tomfothergill.github.io/analytics-agent/>. The Claude Design diagrams are embedded in the architecture section, with standalone SVG versions:

- [Multi-agent orchestration](../../analytics-agent/multi-agent-orchestration.svg)
- [Single-agent loop](../../analytics-agent/single-agent-loop.svg)

Implemented from `Analytics Agent Diagrams.dc.html` in the September 10 handoff. The Python tool's missing return connector was restored. On narrow screens the diagrams scroll horizontally to retain readable labels.

Follow the site's [design system](../../CLAUDE.md), with shared styles in [styles.css](../../styles.css) and [case.css](../../case.css). Article pages use an aubergine background, cream text and orange contact bar. Keep the diagrams anonymous and preserve the distinction between model roles and application controls.

The Markdown copy is a design reference. The published page is static HTML; editing this copy does not automatically update it.
