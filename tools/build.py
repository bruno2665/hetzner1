import csv, json, sys, os

src, tpl, out = sys.argv[1], sys.argv[2], sys.argv[3]

def num(s):
    s = (s or "").strip()
    return float(s) if s else None

rows = []
with open(src, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        rows.append({
            "kategorie": r["kategorie"].strip(),
            "name": r["name"].strip(),
            "preis": num(r["preis"]),
            "vergleich": num(r["vergleich"]),
            "rabatt": int(num(r["rabatt"])) if num(r["rabatt"]) is not None else None,
            "menge": r["menge"].strip(),
            "hinweis": r["hinweis"].strip(),
            "gueltig_von": r["gueltig_von"].strip(),
            "gueltig_bis": r["gueltig_bis"].strip(),
            "url": r["url"].strip(),
        })

# "</" escapen, damit Daten das <script>-Tag nicht beenden koennen
data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
stand = min(r["gueltig_von"] for r in rows)
stand = ".".join(reversed(stand.split("-")))

html = open(tpl, encoding="utf-8").read().replace("__DATA__", data).replace("__STAND__", stand)
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print(f"{len(rows)} Zeilen -> {out} ({os.path.getsize(out)//1024} KB)")
