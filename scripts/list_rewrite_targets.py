# -*- coding: utf-8 -*-
"""재작성 대상(4o-mini 산출 기존 글) 목록 추출 — 제목·URL·카테고리·분량 유지용 메타."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
POSTS = os.path.join(ROOT, "_posts")

# 내가 직접 쓴 글(2026-08-19 이후)은 제외
MINE = {"2026-08-19", "2026-08-20", "2026-08-21", "2026-08-22"}

items = []
for fn in sorted(os.listdir(POSTS)):
    if not fn.endswith(".md"):
        continue
    date = fn[:10]
    if date in MINE:
        continue
    text = open(os.path.join(POSTS, fn), encoding="utf-8").read()
    fm = re.match(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not fm:
        print("front matter 파싱 실패:", fn)
        continue
    head, body = fm.group(1), fm.group(2)

    def field(name):
        m = re.search(rf'^{name}:\s*"?(.*?)"?\s*$', head, re.MULTILINE)
        return m.group(1) if m else ""

    slug = fn[11:-3]
    words = len(re.sub(r"[#*\[\]()>`|!-]", " ", body).split())
    items.append({
        "file": fn,
        "date": date,
        "slug": slug,
        "title": field("title"),
        "category": field("categories").strip("[]"),
        "description": field("description"),
        "tags": field("tags").strip("[]"),
        "words": words,
        "url": f"/{date[:4]}/{date[5:7]}/{date[8:10]}/{slug}/",
    })

with open(os.path.join(ROOT, "rewrite_targets.json"), "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)

print(f"재작성 대상 {len(items)}편 (내가 쓴 4편 제외)")
by_cat = {}
for it in items:
    by_cat[it["category"]] = by_cat.get(it["category"], 0) + 1
print("카테고리 분포:", by_cat)
print("분량:", min(i["words"] for i in items), "~", max(i["words"] for i in items), "words")
for it in items[:5]:
    print(f"  {it['date']} [{it['category']}] {it['title'][:55]} ({it['words']}w)")
