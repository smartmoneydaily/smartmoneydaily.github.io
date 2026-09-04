# -*- coding: utf-8 -*-
"""사람(클로드)이 직접 쓴 원고를 SMD 발행 파이프라인에 주입해 _posts에 저장한다.

쿠마님 지시(2026-08-19): 영어블로그 글도 GPT API로 뽑지 말고 내가 직접 쓴다.
GPT 호출(주제 생성·본문 생성·메타설명)만 건너뛰고, 검증된 후처리는 그대로 태운다:
  품질 검증 → 내부 링크 → 1차 출처 링크 → 툴 삽입 → 핀 이미지 → front matter → 저장

사용:
  python scripts/write_manual_post.py manual_posts.json
manual_posts.json = [{"date":"2026-08-20","title":"...","category":"...","description":"...",
                     "tags":["..."],"content":"markdown 본문(front matter 제외)"}]
"""
import datetime
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from generate_post import (BLOG_NAME, _link_primary_sources, _resolve_bare_brackets,
                           fetch_fdic_national_rates, get_recent_posts_for_linking,
                           get_repo_root, inject_internal_links, inject_tool,
                           load_used_topics, save_used_topics, slugify,
                           validate_post_quality)


def build_post(item, market_data, recent_posts, used_topics):
    title = item["title"].strip()
    category = item["category"].strip()
    content = item["content"].strip()
    date_str = item["date"].strip()
    slug = item.get("slug") or slugify(title)

    problems = validate_post_quality(content, market_data)
    if problems:
        print(f"  [validate] {title[:40]} → {problems}")

    content = inject_internal_links(content, recent_posts, min_links=5, max_links=8)
    content = _resolve_bare_brackets(content, recent_posts)
    rate_cited = bool(market_data) and any(
        re.search(rf"\b{re.escape(r)}%", content) for _, r in market_data["rates"])
    content = _link_primary_sources(content, prefer_rates_page=rate_cited)
    content = inject_tool(content, title, category)

    # 핀 이미지 (실패해도 발행 계속)
    try:
        from generate_blog_pin import generate_pin as _gen_pin
        pin_dir = os.path.join(get_repo_root(), "assets", "pin-images")
        os.makedirs(pin_dir, exist_ok=True)
        pin_filename = f"{date_str}-{slug}.png"
        pin_path = os.path.join(pin_dir, pin_filename)
        _gen_pin(title, BLOG_NAME, category, pin_path)
        content = f"![{title}](/assets/pin-images/{pin_filename})\n\n" + content
        print(f"  pin image: {pin_filename}")
    except Exception as e:
        print(f"  [pin] failed (non-fatal): {e}")

    tags = item.get("tags") or []
    tags = [category] + [t for t in tags if t != category]
    tags_str = ", ".join(dict.fromkeys(tags))

    # 발행 시각: 기존 글을 덮어쓰는 경우 원래 시각을 그대로 유지(발행 이력 보존).
    # 새 글은 저녁 시간대(KST 18~22시 = UTC 09~13시) 안에서 분산.
    if item.get("date_stamp"):
        stamp = item["date_stamp"]
    else:
        rng = random.Random(date_str)
        hh, mm, ss = rng.randint(9, 12), rng.randint(0, 59), rng.randint(0, 59)
        stamp = f"{date_str} {hh:02d}:{mm:02d}:{ss:02d}"

    posts_dir = os.path.join(get_repo_root(), "_posts")
    os.makedirs(posts_dir, exist_ok=True)
    # overwrite: 기존 글의 본문만 교체한다 (URL·색인 보존 — 쿠마님 2026-08-19 지시).
    if item.get("overwrite") and item.get("file"):
        filename = item["file"]
        filepath = os.path.join(posts_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"덮어쓸 원본이 없다: {filename}")
    else:
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(posts_dir, filename)
        suffix = 2
        while os.path.exists(filepath):
            filename = f"{date_str}-{slug}-{suffix}.md"
            filepath = os.path.join(posts_dir, filename)
            suffix += 1
            if suffix > 99:
                break

    description = item["description"].strip().replace('"', "'")
    frontmatter = f"""---
layout: post
title: "{title.replace('"', "'")}"
date: {stamp} +0000
categories: [{category}]
description: "{description}"
tags: [{tags_str}]
---

{content}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)

    used_topics.append(title)
    words = len(re.sub(r"[#*\[\]()>`!-]", " ", content).split())
    print(f"  saved: {filename} ({words} words)")
    return filepath, problems


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "manual_posts.json"
    if not os.path.isabs(src):
        src = os.path.join(get_repo_root(), src)
    items = json.loads(open(src, encoding="utf-8").read())

    market_data = fetch_fdic_national_rates()
    recent_posts = get_recent_posts_for_linking(12)
    used_topics = load_used_topics()

    ok, flagged = 0, []
    for item in sorted(items, key=lambda x: x["date"]):
        print(f"[{item['date']}] {item['title']}")
        try:
            _, problems = build_post(item, market_data, recent_posts, used_topics)
            ok += 1
            if problems:
                flagged.append((item["date"], problems))
        except Exception as e:
            print(f"  FAILED: {type(e).__name__} {e}")
    save_used_topics(used_topics)

    print(f"\n완료: {ok}/{len(items)}편 저장")
    for d, p in flagged:
        print(f"  검증 경고 {d}: {p}")
    sys.exit(0 if ok == len(items) else 1)


if __name__ == "__main__":
    main()
