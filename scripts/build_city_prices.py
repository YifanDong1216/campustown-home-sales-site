"""Rebuild the static homepage from the original CSV (standard library only)."""
import csv
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from html import escape
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
groups = defaultdict(list)
excluded = 0
with (ROOT / 'data/college_town_home_sales.csv').open(newline='', encoding='utf-8') as source:
    for row in csv.DictReader(source):  # Identifiers remain text; only price is converted.
        price = int(row['sale_price'])
        if price < 10_000:
            excluded += 1
            continue
        groups[(row['city'], row['state'])].append(price)

rows = []
for (city, state), prices in sorted(groups.items()):
    value = Decimal(str(median(prices))).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    rows.append(f'          <tr><th scope="row">{escape(city)}, {escape(state)}</th><td>${value:,.0f}</td><td>{len(prices):,}</td></tr>')
included = sum(map(len, groups.values()))
page = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Median home sale price by city</title>
  <link rel="icon" href="data:,">
  <style>
    :root { color-scheme: light; font-family: system-ui, sans-serif; color: #172e3c; background: #f4f7f8; }
    body { max-width: 54rem; margin: auto; padding: 2rem 1rem; line-height: 1.6; }
    h1 { line-height: 1.2; font-size: clamp(1.8rem, 5vw, 2.7rem); }
    .eyebrow { color: #38665d; font-weight: 700; }
    table { width: 100%; border-collapse: collapse; background: white; margin: 2rem 0; font-variant-numeric: tabular-nums; }
    caption { text-align: left; font-weight: 700; margin-bottom: .6rem; }
    th, td { padding: .7rem .6rem; border-bottom: 1px solid #d8e1e5; text-align: right; }
    th:first-child { text-align: left; }
    thead { background: #173e46; color: white; }
    tbody th { font-weight: 500; }
    tbody tr:nth-child(even) { background: #f0f5f5; }
    a { color: #185e70; }
    footer { margin-top: 2rem; font-size: .875rem; color: #435a66; }
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">College-town home sales</p>
    <h1>Median sale price by city</h1>
    <p>Compare completed home sales around university campuses. Prices are in US dollars, rounded to the nearest whole dollar.</p>
    <p>INCLUDED sales across CITIES cities and towns are included.</p>
    <table>
      <caption>City medians after excluding sales under $10,000</caption>
      <thead><tr><th scope="col">City, state</th><th scope="col">Median price</th><th scope="col">Sales included</th></tr></thead>
      <tbody>
ROWS
      </tbody>
    </table>
    <h2>How these prices are calculated</h2>
    <p>We exclude sales below $10,000 because the source contains implausibly low reported prices. This removes EXCLUDED sales. Sales at exactly $10,000 and all higher prices remain included; no upper price limit is applied.</p>
    <p>Each city and state is calculated separately. The median is the middle sale price when prices are sorted; for an even number of sales, it is the average of the two middle prices. Every qualifying sale row is kept, including repeated street addresses that may represent separate units or sales. No filters are applied to dates or property type.</p>
    <p>Source values are as reported, not independently verified against county records. These medians describe the sales in this dataset, not all homes in each city.</p>
    <p><a href="data/college_town_home_sales.csv">Original CSV data</a> · <a href="docs/data_description_sheet.md">Data description and limitations</a></p>
  </main>
  <footer>
    <p>College-town home sales dataset, version 1.0 (2026). University of Illinois-Deloitte Foundation Center for Business Emerging Technologies. Data collected March 2026.</p>
  </footer>
</body>
</html>
'''
page = page.replace('INCLUDED', f'{included:,}').replace('CITIES', str(len(groups))).replace('EXCLUDED', f'{excluded:,}').replace('ROWS', '\n'.join(rows))
(ROOT / 'index.html').write_text(page, encoding='utf-8')
