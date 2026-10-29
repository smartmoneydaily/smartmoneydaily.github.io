# -*- coding: utf-8 -*-
"""신규 글 사후 검증 (read-only, 2026-06-10).

v9/v10 가드(메타 양산단어·promissory 표현·내부링크 permalink·클리셰)가
자동 발행 글에서 실제로 지켜지는지 검사. 수정은 하지 않고 리포트만 출력.

사용: python scripts/verify_recent_posts.py [--since 2026-06-02]
2026-10-28: 2026-11-01 이후 글은 스크립트/humanlike.py scan_en 사람글 검사도 본다(치명 = FAIL). 모듈이 없으면 건너뛴다고 출력.
"""
import os
import re
import sys

# generate_post의 상수 재사용
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from generate_post import _BANNED_META
except Exception:
    _BANNED_META = ("unlock", "discover", "boost", "maximize", "don't miss out",
                    "explore", "dive into", "learn everything", "in this guide",
                    "find out how", "in our comprehensive guide", "the secrets")

PROMISSORY_PAT = re.compile(r"guaranteed returns|risk-free (?:profit|return)|you will earn", re.I)
CLICHE_PAT = re.compile(
    r"In today's fast-paced world|In the modern era|Have you ever wondered|Welcome to my blog|"
    r"Let's dive in|delve into|unlock the secrets|embark on a journey|in the realm of|tapestry of|"
    r"ever-evolving landscape|navigate the world of|treasure trove", re.I)
# 내부 링크: /YYYY/MM/DD/slug/ (또는 /assets/, /tools/) 형식 외의 상대링크 = 404 후보
LINK_PAT = re.compile(r"\]\((/[^)]+)\)")
GOOD_LINK_PAT = re.compile(r"^/(?:\d{4}/\d{2}/\d{2}/[a-z0-9-]+/?|assets/|tools/)")
STYLE_SINCE = "2026-11-01"
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "스크립트"))
    import humanlike
except ImportError:
    humanlike = None


def tokens(text):
    return {t for t in re.sub(r"[^a-z0-9 ]", " ", text.lower()).split() if len(t) >= 3}


def main():
    since = "2026-06-02"
    if "--since" in sys.argv:
        since = sys.argv[sys.argv.index("--since") + 1]

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(repo_root, "_posts")

    results = []
    titles = []
    for fn in sorted(os.listdir(posts_dir)):
        if not fn.endswith(".md") or fn[:10] < since:
            continue
        path = os.path.join(posts_dir, fn)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        fm = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
        front = fm.group(1) if fm else ""
        body = text[fm.end():] if fm else text

        title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front, re.MULTILINE)
        desc_m = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', front, re.MULTILINE)
        title = title_m.group(1) if title_m else fn
        desc = (desc_m.group(1) if desc_m else "").replace("’", "'").lower()
        titles.append((fn, title))

        issues = []
        banned_hits = [b for b in _BANNED_META if b in desc]
        if banned_hits:
            issues.append(f"메타 BANNED: {banned_hits}")
        pm = PROMISSORY_PAT.search(body)
        if pm:
            issues.append(f"promissory: {pm.group(0)!r}")
        cm = CLICHE_PAT.search(body)
        if cm:
            issues.append(f"클리셰: {cm.group(0)!r}")
        bad_links = [l for l in LINK_PAT.findall(body) if not GOOD_LINK_PAT.match(l)]
        if bad_links:
            issues.append(f"의심 내부링크 {len(bad_links)}개: {bad_links[:3]}")
        wc = len(re.findall(r"\b\w+\b", body))
        if wc < 1200:
            issues.append(f"단어수 {wc} < 1200")
        about_n = len(re.findall(r"^##\s+About the Author", body, re.MULTILINE | re.IGNORECASE))
        if about_n:
            issues.append(f"About the Author 섹션 {about_n}개 (v11 이후엔 0이어야)")

        if fn[:10] >= STYLE_SINCE and humanlike is not None:
            issues += ["사람글: " + x for x in humanlike.scan_en(body)[0]]
            issues += ["사람글: " + x for x in humanlike.scan_title_en(title)[0]]   # 10/30 제목 틀도 본다

        results.append((fn, title, wc, issues))

    if humanlike is None:
        print("참고: 사람글 검사 모듈(스크립트/humanlike.py)을 못 찾아 사람글 검사는 건너뜀")
    print(f"=== {since} 이후 {len(results)}편 검증 ===\n")
    fails = 0
    for fn, title, wc, issues in results:
        status = "PASS" if not issues else "FAIL"
        if issues:
            fails += 1
        print(f"[{status}] {fn} ({wc}w)")
        for i in issues:
            print(f"    - {i}")

    # 제목 쌍별 토큰 Jaccard ≥ 0.5 = 유사 반복 의심
    print("\n=== 제목 유사 반복 (Jaccard >= 0.5) ===")
    dup = 0
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            a, b = tokens(titles[i][1]), tokens(titles[j][1])
            if not a or not b:
                continue
            jac = len(a & b) / len(a | b)
            if jac >= 0.5:
                dup += 1
                print(f"  {jac:.2f}  {titles[i][1]}  <->  {titles[j][1]}")
    if not dup:
        print("  없음")

    print(f"\n총 {len(results)}편 중 FAIL {fails}편, 유사 제목 쌍 {dup}건")


if __name__ == "__main__":
    main()
