# -*- coding: utf-8 -*-
"""재작성 워크플로 journal에서 본문을 뽑아 기존 _posts 파일에 덮어쓴다 (URL 보존).

사용: python scripts/apply_rewrites.py <journal.jsonl 경로> [--dry]
검증 ok=false 인 파일은 건너뛰고 사유를 출력한다.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

journal = sys.argv[1]
dry = "--dry" in sys.argv

bodies, verdicts = {}, {}
for line in open(journal, encoding="utf-8", errors="replace"):
    try:
        j = json.loads(line)
    except Exception:
        continue
    if j.get("type") != "result":
        continue
    v = j.get("value", j.get("result"))
    if not isinstance(v, dict):
        continue
    # 배치형({posts:[...]}, {results:[...]})과 단일형({file, content} / {file, ok})을 모두 받는다
    for p in (v.get("posts") or []):
        if p.get("file"):
            bodies[p["file"]] = p
    for r in (v.get("results") or []):
        if r.get("file"):
            verdicts[r["file"]] = r
    if v.get("file"):
        if "content" in v:
            bodies[v["file"]] = v
        elif "ok" in v:
            verdicts[v["file"]] = v

targets = {t["file"]: t for t in json.load(open(os.path.join(ROOT, "rewrite_targets.json"), encoding="utf-8"))}
print(f"본문 {len(bodies)}편 / 검증 {len(verdicts)}편")

items, skipped = [], []
for fn, p in bodies.items():
    v = verdicts.get(fn)
    if v is not None and not v.get("ok"):
        skipped.append((fn, v.get("problems", [])))
        continue
    t = targets.get(fn)
    if not t:
        print("대상 메타 없음:", fn)
        continue
    tags = [x.strip() for x in t["tags"].split(",") if x.strip()]
    items.append({
        "file": fn,
        "overwrite": True,
        "date": t["date"],
        "date_stamp": t["date_stamp"],
        "title": t["title"],
        "category": t["category"],
        "description": p["description"],
        "tags": tags,
        "content": p["content"],
        "slug": t["slug"],
    })

words = {i["file"]: len(re.sub(r"[#*\[\]()>`|-]", " ", i["content"]).split()) for i in items}
for i in items:
    print(f"  적용 대상 {i['date']} {words[i['file']]}w | {i['title'][:45]}")
for fn, probs in skipped:
    print(f"\n  [보류] {fn}")
    for pr in probs[:3]:
        print("     -", str(pr)[:160])

out = os.path.join(ROOT, "rewrite_apply.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
print(f"\n적용 {len(items)}편 / 보류 {len(skipped)}편 → rewrite_apply.json")
if not dry and items:
    os.system(f'python "{os.path.join(ROOT, "scripts", "write_manual_post.py")}" rewrite_apply.json')
