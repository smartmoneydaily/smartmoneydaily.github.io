# -*- coding: utf-8 -*-
"""집필 워크플로 journal에서 원고+검증 판정을 뽑아 manual_posts.json 저장."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JOURNAL = (r"C:\Users\goopy\.claude\projects\C--Users-goopy-Desktop-Claude"
           r"\501d3cd9-b6c3-441e-96fd-e5a2ebf9309c\subagents\workflows\wf_a929d2c1-27f\journal.jsonl")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

posts, verdicts = {}, {}
for line in open(JOURNAL, encoding="utf-8", errors="replace"):
    try:
        j = json.loads(line)
    except Exception:
        continue
    if j.get("type") != "result":
        continue
    val = j.get("value", j.get("result"))
    items = val if isinstance(val, list) else [val]
    for it in items:
        if not isinstance(it, dict):
            continue
        p = it.get("post") if isinstance(it.get("post"), dict) else (it if "content" in it else None)
        if p and p.get("date"):
            posts[p["date"]] = p
            v = it.get("verdict")
            if isinstance(v, dict):
                verdicts[p["date"]] = v

ordered = [posts[d] for d in sorted(posts)]
with open(os.path.join(ROOT, "manual_posts.json"), "w", encoding="utf-8") as f:
    json.dump(ordered, f, ensure_ascii=False, indent=1)

print(f"원고 {len(ordered)}편 저장")
for d in sorted(posts):
    p, v = posts[d], verdicts.get(d, {})
    words = len(re.sub(r"[#*\[\]()>`|-]", " ", p["content"]).split())
    status = "통과" if v.get("ok") else ("반려" if v else "검증없음")
    print(f"\n[{d}] {status} | {words} words | {p['title']}")
    for pr in (v.get("problems") or [])[:4]:
        print("   -", str(pr)[:150])
