"""Render the table-tennis case-study page.

Charts follow Tangerine section 9: every chart sits on an aubergine data
surface, series colours are the existing palette redeployed as ink on that
ground, sign is encoded by fill rather than hue, and interaction is a focus
state with a fixed readout slot -- never a floating tooltip.
"""
import io, json, os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

S = json.load(io.open(os.path.join(HERE, "stats.json"), encoding="utf-8"))

HATCH = "rgba(255,233,204,0.38)"   # --chart-hatch


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def money(v, dp=2):
    return ("+" if v >= 0 else "\u2212") + ("%.*f" % (dp, abs(v)))


# ---------------------------------------------------------------- chart 1
def cumulative_svg():
    """One series, so one colour and no legend (9.6)."""
    pts = S["cumulative"]
    d0 = datetime.strptime(pts[0][0], "%Y-%m-%d")
    xs = [(datetime.strptime(d, "%Y-%m-%d") - d0).days for d, _ in pts]
    ys = [v for _, v in pts]
    W, H = 1000, 300
    L, R, T, B = 54, 16, 14, 34
    span = max(xs) or 1
    ymin, ymax = min(0.0, min(ys)), max(ys) * 1.06

    def px(x):
        return L + (x / span) * (W - L - R)

    def py(y):
        return T + (1 - (y - ymin) / (ymax - ymin)) * (H - T - B)

    # Gridlines: 1px --chart-grid, horizontal only, four maximum (9.5).
    grid = ""
    for g in (400, 800, 1200):
        grid += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>'
                 '<text x="%.1f" y="%.1f" class="tick" text-anchor="end">%d</text>'
                 % (L, py(g), W - R, py(g), L - 10, py(g) + 3, g))

    # Zero line: the only 1.5px stroke in the chart, load-bearing here because
    # the whole claim is distance from zero (9.6).
    zero = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="zero"/>'
            % (L, py(0), W - R, py(0)))

    # A gap of more than 45 days is a change of state, not of subject, so the
    # connector switches to a 3px dash at the same colour and weight (9.3).
    segs, dashes, cur = [], [], [(px(xs[0]), py(ys[0]))]
    for i in range(1, len(xs)):
        a, b = (px(xs[i - 1]), py(ys[i - 1])), (px(xs[i]), py(ys[i]))
        if xs[i] - xs[i - 1] > 45:
            segs.append(cur)
            dashes.append((a, b, xs[i] - xs[i - 1]))
            cur = [b]
        else:
            cur.append(b)
    segs.append(cur)

    paths = "".join(
        '<path class="line" d="M%s"/>' % (" L".join("%.1f %.1f" % p for p in seg))
        for seg in segs if len(seg) > 1)
    paths += "".join(
        '<path class="line line--dash" d="M%.1f %.1f L%.1f %.1f"/>' % (a[0], a[1], b[0], b[1])
        for a, b, _ in dashes)

    # Year ticks: 10px mono, amber. No axis lines drawn (9.5).
    ticks = ""
    for yr in range(d0.year + 1, datetime.strptime(pts[-1][0], "%Y-%m-%d").year + 1):
        dx = (datetime(yr, 1, 1) - d0).days
        if 0 <= dx <= span:
            ticks += ('<text x="%.1f" y="%.1f" class="tick" text-anchor="middle">%d</text>'
                      % (px(dx), H - B + 18, yr))

    # The one permitted annotation: 11px mono cream, 1px cream leader, no
    # arrowhead (9.5). It names the state the dash is already showing.
    note = ""
    if dashes:
        # One annotation per chart, so it goes on the longest dormant span.
        (ax, ay), (bx, by), days = max(dashes, key=lambda d: d[2])
        mx, my = (ax + bx) / 2, (ay + by) / 2
        note = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="leader"/>'
                '<text x="%.1f" y="%.1f" class="annot" text-anchor="middle">'
                '%d MONTHS DORMANT</text>'
                % (mx, my, mx, my + 30, mx, my + 44, round(days / 30.44)))

    focus = ('<line class="guide" x1="0" y1="%.1f" x2="0" y2="%.1f" hidden/>'
             '<circle class="dot" r="4" hidden/>' % (T, H - B))
    hit = ('<rect class="hit" x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
           'fill="none" pointer-events="all"/>' % (L, T, W - L - R, H - T - B))

    series = json.dumps([[round(px(x), 1), round(py(y), 1), d, y]
                         for (d, y), x in zip(pts, xs)], separators=(",", ":"))

    svg = ('<svg class="chart chart--line" viewBox="0 0 1000 %d" tabindex="0" role="img" '
           'aria-label="Cumulative profit in units, March 2021 to April 2024, rising to '
           'plus 1222 units, with a nine-month dormant span through 2023.">'
           '%s%s%s%s%s%s%s</svg>' % (H, grid, zero, paths, note, ticks, focus, hit))
    return svg + ('<script type="application/json" id="cum-series">%s</script>' % series)


# ---------------------------------------------------------------- chart 2
def monthly_svg():
    """Sign by fill: positive solid, negative hollow and hatched (9.7)."""
    ms = S["monthly"]
    W, H = 1000, 250
    L, R, T, B = 54, 16, 14, 38
    vals = [m["profit"] for m in ms]
    ymin, ymax = min(vals) * 1.15, max(vals) * 1.1
    slot = (W - L - R) / len(ms)
    gap = 4.0
    bw = slot - gap

    def py(y):
        return T + (1 - (y - ymin) / (ymax - ymin)) * (H - T - B)

    z = py(0)
    grid = ""
    for g in (-50, 50, 100, 150):
        if ymin < g < ymax:
            grid += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>'
                     '<text x="%.1f" y="%.1f" class="tick" text-anchor="end">%+d</text>'
                     % (L, py(g), W - R, py(g), L - 10, py(g) + 3, g))

    bars, hits, drawn = "", "", 0
    for i, m in enumerate(ms):
        x = L + i * slot + gap / 2
        p = m["profit"]
        if not m["bets"]:
            # Dormant months are context, not a mark: a hairline on the zero line.
            bars += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>'
                     % (x, z, x + bw, z))
            continue
        y, h = (py(p), z - py(p)) if p >= 0 else (z, py(p) - z)
        bars += ('<rect class="bar bar--%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
                 % ("pos" if p >= 0 else "neg", x, y, bw, max(h, 1.5)))
        hits += ('<rect class="hit" x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                 'fill="none" pointer-events="all" data-month="%s" '
                 'data-profit="%.2f" data-bets="%d" data-roi="%s"/>'
                 % (L + i * slot, T, slot, H - T - B, m["month"], p, m["bets"],
                    ("%+.2f%%" % m["roi"]) if m["roi"] is not None else "\u2014"))
        drawn += 1

    zero = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="zero"/>'
            % (L, z, W - R, z))

    ticks = ""
    for i, m in enumerate(ms):
        if m["month"].endswith(("-01", "-07")):
            ticks += ('<text x="%.1f" y="%.1f" class="tick" text-anchor="middle">%s</text>'
                      % (L + i * slot + slot / 2, H - B + 20, m["month"]))

    hatch = ('<defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" '
             'stroke="%s" stroke-width="1"/></pattern></defs>' % HATCH)
    ring = '<rect class="ring" fill="none" hidden/>'

    return ('<svg class="chart chart--bars" viewBox="0 0 1000 %d" tabindex="0" role="img" '
            'aria-label="Monthly profit and loss in units. Solid bars are profitable '
            'months, hollow hatched bars are losing months, hairlines mark months with '
            'no bets.">%s%s%s%s%s%s%s</svg>'
            % (H, hatch, grid, bars, zero, ticks, ring, hits))


# ---------------------------------------------------------------- tables
def league_rows():
    out = ""
    for l in S["leagues"]:
        if l["bets"] < 100:
            continue
        out += ('<tr><td>%s</td><td>%s</td><td>%s</td><td class="n">%s</td>'
                '<td class="n">%s</td><td class="n">%s%%</td></tr>'
                % (esc(l["league"]), l["first"], l["last"], "{:,}".format(l["bets"]),
                   money(l["profit"]), money(l["roi"])))
    return out


def bucket_rows():
    out = ""
    for b in S["buckets"]:
        if b["bets"] < 50:
            continue
        out += ('<tr><td>%s</td><td class="n">%s</td><td class="n">%.1f%%</td>'
                '<td class="n">%.1f%%</td><td class="n">%s</td><td class="n">%s%%</td></tr>'
                % (b["label"], "{:,}".format(b["bets"]), b["implied"], b["hit"],
                   money(b["hit"] - b["implied"], 1), money(b["roi"])))
    return out


def fmt(n):
    return "{:,}".format(n)


HTML = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How I built a table tennis model that beat the bookies</title>
<meta name="description" content="A lockdown project that got slightly out of hand: a model run every day for three years against Eastern European table tennis leagues. 10,382 flat-stake bets, an 11.8% return. Every bet is on the page.">
<meta name="theme-color" content="#ff7a1a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&amp;display=swap">
<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="../case.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='@@HASH@@ff7a1a'/><rect x='4' y='4' width='24' height='24' fill='@@HASH@@330a37'/></svg>">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="rule-bar">
  <a class="rule-bar__name" href="../">Thomas Fothergill</a>
  <nav class="rule-bar__nav" aria-label="Primary">
    <a href="../#work">Work</a>
    <a href="../#notes">Notes</a>
    <a href="../#about">About</a>
    <a href="../#contact">Contact</a>
  </nav>
</header>

<main id="main">

  <section class="opener">
    <p class="eyebrow">Case study &middot; 01 &middot; @@first@@ to @@last@@</p>
    <h1>How I built a table tennis model that beat the bookies.</h1>
    <div class="statement__pair">
      <p class="statement__prose">
        A lockdown project that got slightly out of hand: a model run every day
        for three years against Eastern European table tennis leagues.
        @@bets@@ flat-stake bets, an @@roi1@@% return.
      </p>
      <p class="statement__meta">
        @@bets@@ bets<br>
        @@profit@@ units<br>
        @@roi@@% return
      </p>
    </div>
  </section>

  <div class="band">
    <span>Elo</span><span>Flat stakes</span><span>@@active@@ active months</span>
    <span>@@leagues@@ leagues</span><span>Mean price @@mean@@</span>
    <span>Max drawdown @@dd@@ units</span>
  </div>

  <section class="prose">
    <p>
      Between March 2021 and April 2024 I placed @@bets@@ bets on low-level
      table tennis, one unit on every one, and finished @@profit_plain@@ units up,
      which is an @@roi@@% return on turnover. Only @@hit@@% of the bets won, at
      an average price of @@mean@@, which tells you the model leaned towards
      outsiders. It was never as simple as backing the longer price, though, and
      the bets were only ever a small fraction of the matches on offer.
    </p>
    <p>
      It started in the middle of Covid. Nearly all proper sport had shut down,
      and a smaller and much stranger set of sports started to thrive in its
      place. Small Eastern European table tennis leagues sprang up to feed people
      who needed something to bet on. Forbes ran
      <a href="https://www.forbes.com/sites/barrycollins/2020/06/13/anyone-for-ukrainian-table-tennis-the-shady-sport-that-feeds-online-gambling/">a piece on it in June 2020</a>
      that tells that side of the story better than I can.
    </p>
    <p>
      I started watching. One player in red, one in blue, in an empty sports hall
      with no crowd, and a referee sat to one side who at times looked on the
      verge of falling asleep. The players were often extremely out of shape and
      frequently around 60 years old. They were playing seven or eight matches a
      day, and they did not appear to care much about them. When I had money on
      someone I would sometimes look them up online, with results that did not
      inspire confidence.
    </p>
    <p>
      What I saw, because I'm like this, was a modelling opportunity. Thousands of
      players. Random pairings. No tournament structure, no variance in
      conditions. And matches all day, every day, in enormous volumes, with
      enormous volumes of errant odds to pick off. In modelling terms it was close
      to ideal. In every other sense it was odd.
    </p>
    <p>
      The model I settled on was a simple Elo rating system, the same idea chess
      uses to rank its players. Every player carries a rating, and the difference
      between two players' ratings gives you an expected probability of each of
      them winning. After a match, both ratings move by an amount proportional to
      how far the result was from that expectation, scaled by a constant called
      the K-factor, so a win that was expected shifts the ratings very little and
      an upset shifts them a lot. I used a K-factor of 10, started every new
      player at 1,500, updated on matches rather than individual games, and pooled
      the ratings across all the leagues, because keeping them separate per league
      threw away too much information. Once you have two ratings you have a
      probability, and once you have a probability you have a price of your own to
      set against the bookmaker's. Neither of you is obviously right about any one
      match; you only find out who is more accurate over thousands of them.
    </p>
    <p>
      I set up a daily process. Each day's results went into the engine and the
      ratings updated, the model then priced the next day's fixtures, and where my
      price differed enough from the bookmaker's it emailed me to go and place the
      bet. All of this ran in the cloud on PythonAnywhere. Every bet was tracked,
      every result was logged, and the model was tweaked accordingly, which is why
      this page has real numbers on it rather than remembered ones.
    </p>
    <!-- TODO: what "differed enough" meant in practice (the edge threshold), and
         whether the bets were then placed by hand. -->

    <figure class="plot">
      <p class="plot__title">Cumulative profit, units</p>
      <div class="panel">
        <div class="panel__head">
          <p class="legend"></p>
          <p class="readout" data-default-label="Final" data-default-value="@@profit@@">
            <span class="readout__label">Final</span>
            <span class="readout__value">@@profit@@</span>
          </p>
        </div>
        @@cum@@
      </div>
      <figcaption>Flat 1-unit stakes throughout. @@first@@ to @@last@@. The dashed
      span is nine months in which no bets were placed at all.</figcaption>
    </figure>
  </section>

  <section class="prose">
    <p>It worked, and it worked fairly evenly.</p>
    <div class="scroll">
      <table>
        <thead><tr><th>League</th><th>First bet</th><th>Last bet</th><th class="n">Bets</th>
        <th class="n">Units</th><th class="n">ROI</th></tr></thead>
        <tbody>@@leaguerows@@</tbody>
      </table>
    </div>
    <p class="fine">Leagues with fewer than 100 bets are omitted.</p>
    <p>
      Four of the six came back between 13% and 16%, which is remarkably
      consistent for a model that had no idea which league it was looking at. On
      the women's Setka Cup the identical approach produced essentially nothing:
      630 bets, three units up. On the Czech Liga Pro it lost money. I didn't look
      into why at the time and I'm not going to guess now.
    </p>
    <!-- TODO: any recollection of why the Czech and women's leagues behaved
         differently, or confirm "I never looked" and leave the sentence as is. -->
    <p>
      The standard of play was rarely high, and I noticed a number of cases where
      the odds behaved in ways I could not account for from the table tennis. A
      player would be available at 3.00 before the match, win the first game, and
      then drift out to 5.00 or 6.00, in a best-of-three format where winning the
      first game should be a strong position. I never found out what was going on
      in those matches, and I'll leave you to draw your own conclusions. It is also
      worth saying that a player on their eighth match of the day, who does not
      appear to care much whether they win it, is not well described by a rating.
    </p>
  </section>

  <section class="prose">
    <p>
      Then Russia invaded Ukraine. The TT Cup Ukraine, my second-largest league by
      volume and my best by return, placed its last bet two days before the
      invasion and never came back, the Russian Liga Pro followed within a
      fortnight, and the Czech Liga Pro was gone a few weeks after that, replaced
      by a new league, TT Cup. Within about six weeks I had gone from six leagues
      to two, with the Setka Cup carrying most of the volume, and the return
      roughly halved. After ten months like that, keeping it going stopped being
      worth the effort and I switched it off.
    </p>
    <p>
      The nice thing about a model that emails you is that switching it off is
      easy, and so is switching it back on, which I did the best part of a year
      later for no better reason than that I fancied it again. The frustration
      came back with it. The market I'd returned to was narrower still, almost
      entirely Setka Cup, and while the model itself was fine, still returning
      around 12%, there were far fewer places to point it.
    </p>

    <figure class="plot">
      <p class="plot__title">Monthly profit and loss, units</p>
      <div class="panel">
        <div class="panel__head">
          <p class="legend">
            <span class="key key--pos">Profit</span>
            <span class="key key--neg">Loss</span>
          </p>
          <p class="readout" data-default-label="@@active@@-month net" data-default-value="@@profit@@">
            <span class="readout__label">@@active@@-month net</span>
            <span class="readout__value">@@profit@@</span>
          </p>
        </div>
        @@mon@@
      </div>
      <figcaption>Losing months are hollow and hatched, hanging below the zero line.
      Both sides share one scale. Hairlines mark months with no bets.</figcaption>
    </figure>

    <p>
      In the end my betting adventures were ruined by the (some might say immoral)
      practices of betting companies. My accounts were limited to bets of a penny,
      and that was that. The log stops there.
    </p>
  </section>

  <section class="prose">
    <p>
      It's only now, with the whole log in front of me, that I can see what it was
      actually doing. My working theory while it ran, which I never got round to
      testing properly, was that the outsiders were where the value was, and I put
      it down to punters liking a favourite. The log agrees with me, which is
      nice, right up to the point where it falls off a cliff.
    </p>
    <div class="scroll">
      <table>
        <thead><tr><th>Price band</th><th class="n">Bets</th><th class="n">Implied</th>
        <th class="n">Actual</th><th class="n">Edge</th><th class="n">ROI</th></tr></thead>
        <tbody>@@buckets@@</tbody>
      </table>
    </div>
    <p class="fine">Implied is the mean of 1/price across the band; actual is the realised
    strike rate. Bands with fewer than 50 bets are omitted.</p>
    <p>
      Overall a particularly fun and enjoyable experience building this, and a
      useful one: it's the only model I've built where I can point at @@bets@@
      out-of-sample outcomes and say exactly where it was right and exactly where
      it was not.
    </p>
  </section>

  <section class="prose">
    <h2 class="eyebrow">Every bet</h2>
    <p>
      The whole log, unfiltered and unedited: every match, the price taken, the
      scoreline and the return. Flat one unit throughout, so nothing here is
      Kelly-inflated. @@voids@@ abandoned matches are recorded as full losses
      rather than voids, which understates the return slightly.
    </p>
    <p class="lede-link"><a href="#" id="load">Load the full log &mdash; @@bets@@ rows, 768&nbsp;KB &darr;</a></p>

    <div id="log" hidden>
      <div class="filters">
        <label>Search<input type="search" id="q" placeholder="player" autocomplete="off"></label>
        <label>League<select id="lg"><option value="">All</option></select></label>
        <label>Result<select id="res">
          <option value="">All</option><option value="w">Won</option><option value="l">Lost</option>
        </select></label>
        <label>Min price<input type="number" id="pmin" step="0.25" min="1" placeholder="1.00"></label>
        <label>Max price<input type="number" id="pmax" step="0.25" min="1" placeholder="&infin;"></label>
      </div>
      <p class="fine" id="count" aria-live="polite"></p>
      <div class="scroll">
        <table id="tbl">
          <thead><tr><th>Date</th><th>League</th><th>Match</th><th>Bet</th>
          <th class="n">Price</th><th>Score</th><th class="n">Return</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
      <p class="pager">
        <button id="prev" type="button">&larr; Previous</button>
        <span id="page"></span>
        <button id="next" type="button">Next &rarr;</button>
      </p>
    </div>
  </section>

</main>

<footer class="contact">
  <a class="contact__email" href="mailto:you@example.com">you@example.com</a>
  <nav class="contact__links" aria-label="Elsewhere">
    <a href="https://github.com/tomfothergill/tabletennis">The log on GitHub</a>
    <a href="../">Index</a>
    <span>No newsletter</span>
  </nav>
</footer>

<script>
/* Chart focus states (Tangerine 9.4). The subject is never touched: focusing a
   mark recedes every other mark. Values land in the panel's fixed readout slot,
   which is always present, so nothing shifts when it changes. */
(function () {
  var M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var MM = ['January','February','March','April','May','June','July','August',
            'September','October','November','December'];

  function sign(v, dp) {
    return (v >= 0 ? '+' : '\\u2212') + Math.abs(v).toFixed(dp === undefined ? 2 : dp);
  }
  function set(panel, label, value) {
    var r = panel.querySelector('.readout');
    r.querySelector('.readout__label').textContent = label;
    r.querySelector('.readout__value').textContent = value;
  }
  function reset(panel) {
    var r = panel.querySelector('.readout');
    set(panel, r.getAttribute('data-default-label'), r.getAttribute('data-default-value'));
  }

  /* ---- cumulative line ------------------------------------------------ */
  var line = document.querySelector('.chart--line');
  if (line) {
    var panel = line.closest('.panel');
    var pts = JSON.parse(document.getElementById('cum-series').textContent);
    var guide = line.querySelector('.guide');
    var dot = line.querySelector('.dot');
    var vb = line.viewBox.baseVal;
    var at = -1;

    var focusPoint = function (i) {
      if (i < 0 || i >= pts.length) return;
      at = i;
      var p = pts[i];
      guide.setAttribute('x1', p[0]); guide.setAttribute('x2', p[0]);
      dot.setAttribute('cx', p[0]); dot.setAttribute('cy', p[1]);
      guide.hidden = false; dot.hidden = false;
      var d = p[2].split('-');
      set(panel, (+d[2]) + ' ' + M[+d[1] - 1] + ' ' + d[0], sign(p[3]));
    };
    var clearPoint = function () {
      at = -1; guide.hidden = true; dot.hidden = true; reset(panel);
    };

    line.querySelector('.hit').addEventListener('pointermove', function (e) {
      var box = line.getBoundingClientRect();
      var vx = (e.clientX - box.left) / box.width * vb.width;
      var lo = 0, hi = pts.length - 1;
      while (hi - lo > 1) {
        var mid = (lo + hi) >> 1;
        if (pts[mid][0] < vx) lo = mid; else hi = mid;
      }
      focusPoint((vx - pts[lo][0] < pts[hi][0] - vx) ? lo : hi);
    });
    line.addEventListener('pointerleave', clearPoint);
    line.addEventListener('blur', clearPoint);
    line.addEventListener('keydown', function (e) {
      var step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (e.key === 'PageUp') step = 14;
      if (e.key === 'PageDown') step = -14;
      if (!step) { if (e.key === 'Escape') clearPoint(); return; }
      e.preventDefault();
      focusPoint(Math.max(0, Math.min(pts.length - 1, (at < 0 ? 0 : at) + step)));
    });
  }

  /* ---- monthly bars --------------------------------------------------- */
  var bars = document.querySelector('.chart--bars');
  if (bars) {
    var bpanel = bars.closest('.panel');
    var rects = bars.querySelectorAll('.bar');
    var hits = bars.querySelectorAll('.hit');
    var ring = bars.querySelector('.ring');
    var idx = -1, byKey = false;

    var focusBar = function (i, keyboard) {
      if (i < 0 || i >= hits.length) return;
      idx = i; byKey = !!keyboard;
      var h = hits[i], b = rects[i];
      bars.classList.add('is-focusing');
      Array.prototype.forEach.call(rects, function (r) { r.classList.remove('is-focus'); });
      b.classList.add('is-focus');
      if (keyboard) {
        ring.setAttribute('x', +b.getAttribute('x') - 2);
        ring.setAttribute('y', +b.getAttribute('y') - 2);
        ring.setAttribute('width', +b.getAttribute('width') + 4);
        ring.setAttribute('height', +b.getAttribute('height') + 4);
        ring.hidden = false;
      } else {
        ring.hidden = true;
      }
      var ym = h.getAttribute('data-month').split('-');
      set(bpanel, MM[+ym[1] - 1] + ' ' + ym[0] + ' \\u00b7 '
          + (+h.getAttribute('data-bets')).toLocaleString() + ' bets',
          sign(+h.getAttribute('data-profit')));
    };
    var clearBar = function () {
      idx = -1; byKey = false; ring.hidden = true;
      bars.classList.remove('is-focusing');
      Array.prototype.forEach.call(rects, function (r) { r.classList.remove('is-focus'); });
      reset(bpanel);
    };

    Array.prototype.forEach.call(hits, function (h, i) {
      h.addEventListener('pointerenter', function () { focusBar(i, false); });
    });
    bars.addEventListener('pointerleave', function () { if (!byKey) clearBar(); });
    bars.addEventListener('blur', clearBar);
    bars.addEventListener('keydown', function (e) {
      var step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!step) { if (e.key === 'Escape') clearBar(); return; }
      e.preventDefault();
      focusBar(Math.max(0, Math.min(hits.length - 1, (idx < 0 ? -1 : idx) + step)), true);
    });
  }
})();
</script>

<script>
(function () {
  var PAGE = 100, data = null, view = [], page = 0;
  var $ = function (id) { return document.getElementById(id); };

  $('load').addEventListener('click', function (e) {
    e.preventDefault();
    this.textContent = 'Loading\\u2026';
    var self = this;
    fetch('bets.json').then(function (r) { return r.json(); }).then(function (d) {
      data = d;
      d.leagues.forEach(function (l, i) {
        var o = document.createElement('option');
        o.value = i; o.textContent = l; $('lg').appendChild(o);
      });
      self.parentNode.hidden = true;
      $('log').hidden = false;
      apply();
    }).catch(function () { self.textContent = 'Could not load the log. Retry?'; });
  });

  ['q', 'lg', 'res', 'pmin', 'pmax'].forEach(function (id) {
    document.addEventListener('input', function (e) {
      if (e.target.id === id) { page = 0; apply(); }
    });
  });
  $('prev').addEventListener('click', function () { if (page > 0) { page--; draw(); } });
  $('next').addEventListener('click', function () {
    if ((page + 1) * PAGE < view.length) { page++; draw(); }
  });

  function apply() {
    var q = $('q').value.trim().toLowerCase(),
        lg = $('lg').value, res = $('res').value,
        lo = parseFloat($('pmin').value), hi = parseFloat($('pmax').value);
    view = data.rows.filter(function (r) {
      if (lg !== '' && r[1] !== +lg) return false;
      if (res === 'w' && r[7] <= 0) return false;
      if (res === 'l' && r[7] > 0) return false;
      if (!isNaN(lo) && r[5] < lo) return false;
      if (!isNaN(hi) && r[5] > hi) return false;
      if (q && (r[2] + ' ' + r[3]).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    draw();
  }

  function draw() {
    var body = document.querySelector('#tbl tbody'), out = '';
    var slice = view.slice(page * PAGE, page * PAGE + PAGE);
    slice.forEach(function (r) {
      var backed = r[4] === 0 ? r[2] : (r[4] === 1 ? r[3] : '\\u2014');
      var won = r[7] > 0;
      out += '<tr class="' + (won ? 'won' : 'lost') + '"><td class="n">' + r[0] + '</td><td>'
        + esc(data.leagues[r[1]]) + '</td><td>' + esc(r[2]) + ' v ' + esc(r[3])
        + '</td><td>' + esc(backed) + '</td><td class="n">' + num(r[5], 2)
        + '</td><td class="n">' + esc(r[6]) + '</td><td class="n">'
        + (won ? '+' + num(r[7] - 1, 2) : '\\u22121.00') + '</td></tr>';
    });
    body.innerHTML = out;
    var staked = view.length, ret = view.reduce(function (a, r) { return a + r[7]; }, 0);
    var wins = view.reduce(function (a, r) { return a + (r[7] > 0 ? 1 : 0); }, 0);
    $('count').textContent = staked
      ? view.length.toLocaleString() + ' bets \\u00b7 ' + (wins / staked * 100).toFixed(1)
        + '% strike \\u00b7 ' + (ret - staked >= 0 ? '+' : '') + (ret - staked).toFixed(2)
        + ' units \\u00b7 ' + ((ret - staked) / staked * 100).toFixed(2) + '% ROI'
      : 'No bets match those filters.';
    var pages = Math.max(1, Math.ceil(view.length / PAGE));
    $('page').textContent = (page + 1) + ' / ' + pages;
    $('prev').disabled = page === 0;
    $('next').disabled = page + 1 >= pages;
  }

  function num(v, dp) {
    var s = v.toFixed(3);
    return s.slice(-1) === '0' ? v.toFixed(dp) : s;
  }

  function esc(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c];
    });
  }
})();
</script>
</body>
</html>
"""

vals = {
    "first": S["first"], "last": S["last"],
    "bets": fmt(S["bets"]),
    "profit": money(S["profit"]),
    "roi": "%.2f" % S["roi"],
    "roi1": "%.1f" % S["roi"],
    "hit": "%.2f" % S["hit_rate"],
    "profit_plain": "{:,.2f}".format(S["profit"]),
    "active": str(S["active_months"]),
    "leagues": str(len([l for l in S["leagues"] if l["bets"] >= 100])),
    "mean": "%.2f" % S["mean_price"],
    "dd": "%.0f" % S["max_drawdown"],
    "voids": str(S["voids"]),
    "cum": cumulative_svg(), "mon": monthly_svg(),
    "buckets": bucket_rows(), "leaguerows": league_rows(),
    "HASH": "%23",
}
page = HTML
for k, v in vals.items():
    page = page.replace("@@" + k + "@@", v)
assert "@@" not in page, page[page.index("@@"):page.index("@@") + 60]

out_dir = os.path.join(SITE, "table-tennis")
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out_dir, os.path.getsize(os.path.join(out_dir, "index.html")), "bytes")
