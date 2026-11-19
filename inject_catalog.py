"""Embed book_catalog.json into the two pages.

Usage: python3 -I inject_catalog.py <catalog.json> <page.html> [<page.html> ...]
Each page must contain the placeholder line  const CATALOG = __CATALOG__;
or an earlier injected  const CATALOG = [...];  line, which is replaced.
"""
import json
import re
import sys

catalog_path, *pages = sys.argv[1:]
books = json.load(open(catalog_path, encoding="utf-8"))["books"]
keep = ["id", "title", "author", "genre", "blurb", "clues", "sourceList"]
import os
# Covers sit next to index.html (BK001.avif, BK002.jpg, ...), the same flat
# layout GitHub's website upload produces.
cover_dir = os.path.dirname(os.path.abspath(pages[0]))
on_disk = {os.path.splitext(f)[0]: f for f in os.listdir(cover_dir)
           if re.fullmatch(r"BK\d+\.(avif|jpe?g|png|webp)", f)}
slim = []
for b in books:
    row = {k: b[k] for k in keep}
    if b["id"] in on_disk:
        row["cover"] = on_disk[b["id"]]
    slim.append(row)
payload = json.dumps(slim, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
line = "const CATALOG = " + payload + ";"

for page in pages:
    html = open(page, encoding="utf-8").read()
    new, n = re.subn(r"^const CATALOG = .*;$", lambda m: line, html, count=1, flags=re.M)
    if n != 1:
        sys.exit(f"{page}: no CATALOG line found")
    open(page, "w", encoding="utf-8").write(new)
    print(f"{page}: embedded {len(slim)} books")
