"""Build the table-tennis case-study assets from the raw bet log.

Reads Model_Assessment.csv, emits:
  - stats.json      headline figures + monthly series + daily cumulative
  - bets.json       compact match log for the browsable table
"""
import csv, json, io, os, sys
from collections import OrderedDict, defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = HERE
PUBLISHED = os.path.join(ROOT, "table-tennis")

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "Model_Assessment.csv")
if not os.path.isfile(SRC):
    sys.exit(
        "Cannot find the bet log. Clone it and pass the path:\n"
        "  gh repo clone tomfothergill/tabletennis\n"
        "  python build/build_stats.py tabletennis/Model_Assessment.csv")

rows = []
with io.open(SRC, encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        t = r["Time"].strip()
        dt = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S"):
            try:
                dt = datetime.strptime(t, fmt); break
            except ValueError:
                continue
        if dt is None:
            continue
        try:
            price = float(r["Price"]); ret = float(r["Returns"]); stake = float(r["Unit_Stake"])
        except (ValueError, TypeError):
            continue
        rows.append({
            "dt": dt,
            "league": (r["League"] or "").strip(),
            "p1": (r["Player_1"] or "").strip(),
            "p2": (r["Player_2"] or "").strip(),
            "bet": (r["Bet"] or "").strip(),
            "price": price,
            "winner": (r["Winner"] or "").strip(),
            "score": (r["Scoreline"] or "").strip(),
            "ret": ret,
            "stake": stake,
        })

rows.sort(key=lambda x: x["dt"])

n = len(rows)
staked = sum(r["stake"] for r in rows)
returned = sum(r["ret"] for r in rows)
profit = returned - staked
wins = sum(1 for r in rows if r["ret"] > 0)
voids = sum(1 for r in rows if r["winner"].lower() in ("no result", "noresult", ""))
mean_price = sum(r["price"] for r in rows) / n

# ---- monthly ---------------------------------------------------------
monthly = OrderedDict()
for r in rows:
    k = r["dt"].strftime("%Y-%m")
    m = monthly.setdefault(k, {"month": k, "bets": 0, "staked": 0.0, "ret": 0.0})
    m["bets"] += 1; m["staked"] += r["stake"]; m["ret"] += r["ret"]

# fill gap months so the dead zone is visible rather than collapsed away
first = datetime.strptime(next(iter(monthly)), "%Y-%m")
last = datetime.strptime(list(monthly)[-1], "%Y-%m")
full = OrderedDict()
y, mo = first.year, first.month
while (y, mo) <= (last.year, last.month):
    k = "%04d-%02d" % (y, mo)
    full[k] = monthly.get(k, {"month": k, "bets": 0, "staked": 0.0, "ret": 0.0})
    mo += 1
    if mo == 13:
        mo = 1; y += 1
for m in full.values():
    m["profit"] = round(m["ret"] - m["staked"], 2)
    m["roi"] = round((m["ret"] - m["staked"]) / m["staked"] * 100, 2) if m["staked"] else None
    m["staked"] = round(m["staked"], 2); m["ret"] = round(m["ret"], 2)

# ---- daily cumulative ------------------------------------------------
daily = defaultdict(float)
for r in rows:
    daily[r["dt"].strftime("%Y-%m-%d")] += r["ret"] - r["stake"]
cum, run = [], 0.0
for d in sorted(daily):
    run += daily[d]
    cum.append([d, round(run, 2)])

# ---- drawdown --------------------------------------------------------
peak, max_dd, dd_at = -1e9, 0.0, None
for d, v in cum:
    peak = max(peak, v)
    if peak - v > max_dd:
        max_dd, dd_at = peak - v, d

# ---- leagues ---------------------------------------------------------
lg = defaultdict(lambda: {"bets": 0, "staked": 0.0, "ret": 0.0})
for r in rows:
    a = lg[r["league"]]; a["bets"] += 1; a["staked"] += r["stake"]; a["ret"] += r["ret"]
leagues = sorted(
    ({"league": k, "bets": v["bets"], "profit": round(v["ret"] - v["staked"], 2),
      "roi": round((v["ret"] - v["staked"]) / v["staked"] * 100, 2) if v["staked"] else None}
     for k, v in lg.items()),
    key=lambda x: -x["bets"])

# ---- price buckets ---------------------------------------------------
BUCKETS = [(1.0, 1.75), (1.75, 2.5), (2.5, 3.5), (3.5, 5.0), (5.0, 8.0), (8.0, 1e9)]
buckets = []
for lo, hi in BUCKETS:
    sel = [r for r in rows if lo <= r["price"] < hi]
    if not sel:
        continue
    s = sum(r["stake"] for r in sel); rt = sum(r["ret"] for r in sel)
    w = sum(1 for r in sel if r["ret"] > 0)
    buckets.append({
        "label": ("%.2f+" % lo) if hi > 1e8 else ("%.2f-%.2f" % (lo, hi)),
        "bets": len(sel),
        "hit": round(w / len(sel) * 100, 1),
        "implied": round(sum(1 / r["price"] for r in sel) / len(sel) * 100, 1),
        "profit": round(rt - s, 2),
        "roi": round((rt - s) / s * 100, 2) if s else None,
    })

stats = {
    "bets": n,
    "staked": round(staked, 2),
    "returned": round(returned, 2),
    "profit": round(profit, 2),
    "roi": round(profit / staked * 100, 2),
    "hit_rate": round(wins / n * 100, 2),
    "mean_price": round(mean_price, 2),
    "implied_prob": round(sum(1 / r["price"] for r in rows) / n * 100, 2),
    "voids": voids,
    "first": rows[0]["dt"].strftime("%Y-%m-%d"),
    "last": rows[-1]["dt"].strftime("%Y-%m-%d"),
    "active_months": sum(1 for m in full.values() if m["bets"] > 0),
    "span_months": len(full),
    "max_drawdown": round(max_dd, 2),
    "max_drawdown_at": dd_at,
    "monthly": list(full.values()),
    "cumulative": cum,
    "leagues": leagues,
    "buckets": buckets,
}

with io.open(os.path.join(OUT, "stats.json"), "w", encoding="utf-8") as fh:
    json.dump(stats, fh, separators=(",", ":"))

# ---- compact bet log -------------------------------------------------
league_idx = {l["league"]: i for i, l in enumerate(leagues)}
bets = [[r["dt"].strftime("%Y-%m-%d %H:%M"), league_idx[r["league"]], r["p1"], r["p2"],
         0 if r["bet"] == r["p1"] else (1 if r["bet"] == r["p2"] else 2),
         r["price"], r["score"], round(r["ret"], 3)] for r in rows]
with io.open(os.path.join(PUBLISHED, "bets.json"), "w", encoding="utf-8") as fh:
    json.dump({"leagues": [l["league"] for l in leagues], "rows": bets}, fh, separators=(",", ":"))

print(json.dumps({k: v for k, v in stats.items()
                  if k not in ("monthly", "cumulative", "leagues", "buckets")}, indent=2))
print("\nleagues:", json.dumps(leagues[:8], indent=1))
print("\nbuckets:", json.dumps(buckets, indent=1))
print("\nmonths:", len(full), "cum points:", len(cum))
print("sizes:", os.path.getsize(os.path.join(OUT, "stats.json")),
      os.path.getsize(os.path.join(PUBLISHED, "bets.json")))
