# -*- coding: utf-8 -*-
"""수동 집필용 컨텍스트 덤프: FDIC 실데이터 + 최근 글(내부링크용) + 기사용 주제 목록."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from generate_post import (fetch_fdic_national_rates, get_existing_slugs,
                           get_recent_posts_for_linking, load_used_topics)

market = fetch_fdic_national_rates()
recent = get_recent_posts_for_linking(12)
used = load_used_topics()

out = {
    "fdic": market,
    "recent_posts": recent,
    "used_topics": used[-40:],
    "existing_slug_count": len(get_existing_slugs()),
}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "manual_context.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("FDIC:", json.dumps(market, ensure_ascii=False) if market else "없음")
print(f"최근 글 {len(recent)}건 / 사용 주제 {len(used)}건 / 기존 slug {out['existing_slug_count']}")
print("저장:", os.path.abspath(path))
