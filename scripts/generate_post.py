"""
SmartMoneyDaily Auto Post Generator v8 (2026-05-23) — AdSense re-approval rebuild
- Single narrow niche: high-yield savings, CDs, money market accounts (US)
- ACCURACY FIRST: no fabricated numbers, dates, personal results, or current APYs
- Public 1st-party sources (FDIC / Federal Reserve / CFPB / NCUA / Treasury) by name
- used_topics.json prevents duplicate content; internal linking kept for SEO
"""

import datetime
import html as _htmllib
import json
import os
import random
import re
import time
import urllib.parse
import urllib.request

BLOG_NAME = "SmartMoneyDaily"
BLOG_NICHE = "high-yield savings accounts, CDs, and money market accounts"
BLOG_DESCRIPTION = "Plain-English guides to high-yield savings accounts, CDs, and money market accounts, built from public FDIC and Federal Reserve information."

CATEGORIES = [
    "high-yield-savings",     "cd-rates",     "money-market",     "fdic-insurance",
    "savings-strategy",     "bank-comparison",     "interest-rates",     "emergency-fund",
]

# {YEAR} is a literal placeholder; it is substituted at call time (see _generate_post_content_inner).
SYSTEM_PROMPT = """You are a personal finance writer for SmartMoneyDaily, a site focused narrowly on
high-yield savings accounts (HYSAs), certificates of deposit (CDs), and money market accounts in the United States.

Your job: write accurate, genuinely useful, AdSense-quality explainers that a careful reader can trust —
written like a knowledgeable human, not generic AI filler.

ACCURACY — THE #1 RULE (this is exactly what gets finance sites approved or rejected):
- Do NOT invent specific dollar amounts, dates, personal results, account names, or test outcomes.
- Do NOT fabricate a personal anecdote (e.g. "In 2023 I moved $4,200 into..."). If you did not do it, do not claim it.
- Use ONLY:
  (a) general facts stated as ranges or typical behavior ("online banks usually pay meaningfully more than the national average"),
  (b) named public reference points that are stable and verifiable (FDIC standard deposit insurance is $250,000 per depositor,
      per insured bank, per ownership category; the FDIC publishes national-average deposit rates; the Federal Reserve sets the
      federal funds rate; NCUA insures credit unions),
  (c) clearly hypothetical examples explicitly labeled ("For example, if you kept $10,000 in an account earning 4% APY,
      that would be about $400 in a year before tax").
- Never state a specific CURRENT APY as a fact (rates change constantly). Instead explain how to find and compare current rates.
  The ONLY exception: numbers explicitly listed in a "VERIFIED CURRENT DATA" block in the user message — those are official
  FDIC national averages fetched at build time. Cite them WITH their as-of date, and only where they genuinely strengthen the point.
- Do NOT state a numeric pass-through ratio between Federal Reserve rate moves and account APYs (e.g., "a 0.25% Fed hike adds about 0.1-0.3% to your APY"). No authority publishes such a fixed ratio and it cannot be verified. Describe the relationship qualitatively only (when the Fed raises rates, deposit yields generally tend to rise too, but the timing and amount vary by institution).
- All examples and references must be consistent with the current year {YEAR}. Never cite a past personal result with a specific date.
- Accuracy note: the Federal Reserve suspended Regulation D's six-per-month savings/money-market withdrawal limit in 2020.
  Do NOT present a federal "six withdrawals per month" rule as if it is current. Describe withdrawal limits as set by each
  individual bank or credit union (some still impose their own limits).
- Do NOT use promotional or promissory phrasing such as "guaranteed returns", "risk-free profit", or "you will earn".
  A CD pays a fixed, contractual interest rate and (within FDIC limits) protects principal — describe that precisely as a
  "fixed interest rate" or "guaranteed interest rate", never as "guaranteed returns" on an "investment".

Writing rules:
- Friendly, clear, authoritative tone. Short paragraphs (2-3 sentences).
- Use ## for H2 and ### for H3. Bullet/numbered lists where they aid comprehension.
- Naturally use the main keyword 4-6 times — no keyword stuffing.
- Open with a concrete, specific hook (a common mistake, a number that is generally true, or the core question) —
  never a generic "In today's world" intro.
- End with a clear, actionable next step.
- Do NOT output a markdown "# Title". Do NOT add AI disclaimers or an "About the Author" section inside the article body (author info and the transparency note are shown by the site layout, not inside the article).

ANTI-AI-CLICHE (these phrases trigger reviewers' "low-value AI" flag — never use):
- "In today's fast-paced world", "In the modern era", "It's no secret that", "Have you ever wondered",
  "Welcome to my blog", "Let's dive in", "delve into", "navigate the world of", "unlock the secrets",
  "embark on a journey", "treasure trove", "in the realm of", "tapestry of", "ever-evolving landscape",
  "in today's market", "when it comes to", "the world of personal finance", "navigating the complexities",
  "can feel daunting", "can feel overwhelming".
- Avoid empty filler: "It is important to note that", "It goes without saying", "Needless to say".

VOICE / E-E-A-T (honest version — do NOT fabricate):
- You may use a light editorial first-person voice to show judgment ("Here's how I'd compare them", "What I'd check first",
  "In my view") — but NEVER invented personal financial results or fake test stories.
- Demonstrate expertise through accurate explanation of mechanics (how APY compounding works, how CD early-withdrawal
  penalties work, how FDIC coverage is calculated across ownership categories), not through made-up anecdotes.

SOURCES (build trust without fabrication):
- Reference real, well-known public authorities by name where relevant: FDIC, the Federal Reserve, the Consumer Financial
  Protection Bureau (CFPB), the U.S. Treasury, the National Credit Union Administration (NCUA). Cite what each one actually
  provides ("the FDIC's BankFind Suite lets you confirm a bank is insured").
- Do NOT fabricate URLs, study titles, or specific statistics. Name the organization and what it does; never invent a number
  and attribute it to them.

INFORMATION GAIN (make it genuinely more useful than a thin AI page):
- Prefer concrete mechanics (how compounding is calculated step by step, how a CD penalty is computed,
  how FDIC coverage stacks across ownership categories) over abstract advice anyone could write.
- When the STRUCTURE PLAN asks for a comparison table, compare real, stable attributes
  (e.g., liquidity, how the rate behaves, FDIC coverage, best use case) — each cell a short complete phrase.

STRUCTURE:
- Follow the STRUCTURE PLAN in the user message for THIS article exactly. Articles on this site
  intentionally vary in structure — do NOT fall back to one fixed skeleton you used before.
- Never output a markdown "# Title" line, and never add an "About the Author" section in the body
  (author info is rendered by the site layout; repeating it in every article is a mass-production signal).
"""




def get_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def load_used_topics():
    """Load previously used topic slugs."""
    filepath = os.path.join(get_repo_root(), "scripts", "used_topics.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_used_topics(topics):
    filepath = os.path.join(get_repo_root(), "scripts", "used_topics.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)


def get_existing_slugs():
    """Get all existing post slugs from _posts/."""
    posts_dir = os.path.join(get_repo_root(), "_posts")
    slugs = set()
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            if filename.endswith(".md"):
                # Remove date prefix and .md suffix
                slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", filename[:-3])
                # Normalize: remove trailing random numbers
                slug = re.sub(r"-\d{2,3}$", "", slug)
                slugs.add(slug)
    return slugs


def get_living_titles():
    """현재 살아 있는 글의 제목 전부.

    v14(2026-07-28): 중복 판정 기준을 used_topics(누적 이력, 통합 후 실제와 어긋남)에서
    '지금 사이트에 실제로 떠 있는 글'로 옮긴다. 123편을 29편 결정판으로 통합한 뒤
    used_topics 에는 이미 사라진 제목 281개가 남아 있어, 그것만 보고 중복을 재던 방식은
    새 글이 결정판과 같은 검색의도를 다시 파고드는 걸 막지 못했다.
    """
    posts_dir = os.path.join(get_repo_root(), "_posts")
    titles = []
    if not os.path.exists(posts_dir):
        return titles
    for filename in sorted(os.listdir(posts_dir)):
        if not filename.endswith(".md"):
            continue
        try:
            with open(os.path.join(posts_dir, filename), "r", encoding="utf-8") as f:
                head = f.read(1200)
        except OSError:
            continue
        m = re.search(r'^title:\s*"(.+?)"\s*$', head, re.M)
        if m:
            titles.append(m.group(1))
    return titles


def get_recent_posts_for_linking(limit=10):
    """Return list of dicts {title, slug, url} for internal linking context.
    url은 실제 permalink(/{BLOG}/:year/:month/:day/:title/) — slug만으로 링크하면 404 (permalink가 날짜 포함)."""
    posts_dir = os.path.join(get_repo_root(), "_posts")
    posts = []
    if os.path.exists(posts_dir):
        files = sorted(os.listdir(posts_dir), reverse=True)
        for filename in files[:limit]:
            m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", filename)
            if not m:
                continue
            y, mo, d, slug = m.groups()
            url = f"/{y}/{mo}/{d}/{slug}/"
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
                        posts.append({"title": title, "slug": slug, "url": url})
                        break
    return posts


def get_recent_titles(limit=10):
    return [p["title"] for p in get_recent_posts_for_linking(limit)]


# inject_internal_links v2 (2026-04-21): exact title + partial-phrase match + Further Reading fallback
def inject_internal_links(content, recent_posts, min_links=3, max_links=5):
    """Weave internal links into the post. Strategy:
    1) Exact title match → wrap in a Markdown link
    2) If title didn't appear verbatim, try the first 3-5 meaningful words as a phrase
    3) If total inserted links < min_links, append a '## Further Reading' list at the end
    """
    if not recent_posts:
        return content

    inserted_slugs = set()
    STOPWORDS = {"the", "a", "an", "for", "and", "with", "to", "of", "in", "on", "at", "is", "are", "my"}

    def already_linked(url):
        return f"]({url})" in content

    # Pass 1: exact title
    for rp in recent_posts:
        if len(inserted_slugs) >= max_links:
            break
        title = rp.get("title", "")
        slug = rp.get("slug", "")
        url = rp.get("url", "")
        if not title or not slug or not url or already_linked(url):
            continue
        if title not in content:
            continue
        safe_title = re.escape(title)
        pattern = re.compile(r"(?<!\]\()(?<!\[)" + safe_title + r"(?!\])")
        new_content, n = pattern.subn(f"[{title}]({url})", content, count=1)
        if n:
            content = new_content
            inserted_slugs.add(slug)

    # Pass 2: partial phrase (first 3-5 meaningful words, case-insensitive)
    for rp in recent_posts:
        if len(inserted_slugs) >= max_links:
            break
        title = rp.get("title", "")
        slug = rp.get("slug", "")
        url = rp.get("url", "")
        if not title or not slug or not url or slug in inserted_slugs or already_linked(url):
            continue
        words = [w for w in re.findall(r"[A-Za-z0-9']+", title)
                 if w.lower() not in STOPWORDS and len(w) > 1]
        if len(words) < 3:
            continue
        for window in (5, 4, 3):
            if len(words) < window:
                continue
            phrase_words = words[:window]
            phrase_pattern = r"(?<!\]\()(?<!\[)" + r"\s+".join(map(re.escape, phrase_words)) + r"(?!\])"
            m = re.search(phrase_pattern, content, flags=re.IGNORECASE)
            if m:
                matched = m.group(0)
                content = content[: m.start()] + f"[{matched}]({url})" + content[m.end():]
                inserted_slugs.add(slug)
                break

    # Fallback: append Further Reading if we still don't have enough links
    if len(inserted_slugs) < min_links:
        remaining = [rp for rp in recent_posts
                     if rp.get("slug") and rp.get("url") and rp["slug"] not in inserted_slugs
                     and not already_linked(rp["url"])]
        need = max(min_links - len(inserted_slugs), 3)
        picks = remaining[:need]
        if picks:
            block = "\n\n## Further Reading\n\n"
            for rp in picks:
                block += f"- [{rp['title']}]({rp['url']})\n"
            content = content.rstrip() + block

    return content


def slugify(title):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


# === v15 (2026-08-02) — market signals: 실데이터(FDIC) + 뉴스 신선도 ==========
# 색인 거부의 지목 원인이 '정보이득 부재'(수치 전면 금지로 어느 글에도 현재 시장 맥락이 없음).
# 해법: 발행 시점에 FDIC 공식 전국 평균 금리를 실측해 '검증된 수치'로만 주입하고(기준일 명기),
# 구글 뉴스 헤드라인으로 주제·본문에 시의성 각도를 공급한다. 두 소스 모두 실패 시 기존
# 동작으로 폴백 — 발행 0 위험 없음 (티스토리봇 네이버 파이프라인과 같은 원칙).
_FDIC_RATES_URL = "https://www.fdic.gov/national-rates-and-rate-caps"
_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
_NEWS_QUERIES = (
    "high-yield savings account rates",
    "CD rates Federal Reserve",
    "money market account rates",
)
_FDIC_PRODUCTS = (
    "Savings", "Interest Checking", "Money Market", "1 month CD", "3 month CD",
    "6 month CD", "12 month CD", "24 month CD", "36 month CD", "48 month CD", "60 month CD",
)


def _http_get(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SMD-build/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_fdic_national_rates():
    """FDIC 공식 전국 평균 예금금리 페이지 실측 파싱.

    반환: {"as_of": "July 20, 2026", "rates": [("Savings", "0.38"), ...]} 또는 None.
    셀 값은 `\\d{1,2}.\\d{2}` 정확 매칭만 채택 — 실측에서 각주 마커가 섞인 '4.15.4' 같은
    오염 셀이 있었고, 그런 행은 버린다. 유효 행 4개 미만이면 페이지 구조가 바뀐 것으로
    보고 None (데이터 없이 발행 계속)."""
    def _clean_cell(c):
        # 태그 제거 → 엔티티 해제 → 공백 정규화 → 각주 숫자 꼬리 제거 ('Savings1' → 'Savings')
        c = _htmllib.unescape(re.sub(r"<[^>]+>", "", c))
        c = re.sub(r"\s+", " ", c.replace("\xa0", " ")).strip()
        return re.sub(r"(?<=[A-Za-z])\d+$", "", c).strip()

    try:
        page = _http_get(_FDIC_RATES_URL)
        # 기준일은 태그 스트립한 전체 텍스트에서 탐색 (날짜와 'as of' 사이 태그에 안 깨지게 — codex)
        text = re.sub(r"\s+", " ", _htmllib.unescape(re.sub(r"<[^>]+>", " ", page)))
        m = re.search(r"(?:as of|updated)\D{0,40}?([A-Z][a-z]+ \d{1,2}, \d{4})", text, re.I)
        if not m:
            print("[fdic] skipped: as-of date not found")
            return None
        as_of = m.group(1)
        rates = []
        header_ok = False
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
            cells = [_clean_cell(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
            if len(cells) < 2:
                continue
            # 열 순서 검증: 2열이 전국평균이 맞는지 헤더로 확인 — 열이 재배치되면 엉뚱한
            # 수치(rate cap 등)를 '전국평균'으로 인용하게 되므로 fail-closed (codex)
            if cells[0].lower().startswith("deposit product") and cells[1].lower().startswith("national deposit rate"):
                header_ok = True
                continue
            if cells[0] in _FDIC_PRODUCTS and re.fullmatch(r"\d{1,2}\.\d{2}", cells[1]):
                rates.append((cells[0], cells[1]))
        if not header_ok:
            print("[fdic] skipped: national-rate header column not verified")
            return None
        if len(rates) < 4:
            print(f"[fdic] skipped: only {len(rates)} valid rows")
            return None
        return {"as_of": as_of, "rates": rates}
    except Exception as e:
        print(f"[fdic] fetch failed (non-fatal): {e}")
        return None


def fetch_news_headlines(limit=10, max_age_days=10):
    """구글 뉴스 RSS(영문)에서 니치 관련 최신 헤드라인 수집. 실패/0건이면 [] — 발행 계속.

    헤드라인은 신뢰 불가 외부 데이터로 취급: 제어문자 제거·공백 정규화·길이 제한,
    발행일 파싱 실패 항목은 신선도 보장 불가라 제외. ' - 매체명' 꼬리는 제거."""
    out, seen = [], set()
    now = datetime.datetime.now()
    for q in _NEWS_QUERIES:
        try:
            xml = _http_get(_NEWS_RSS.format(query=urllib.parse.quote(q)), timeout=10)
        except Exception as e:
            print(f"[news] '{q}' failed (non-fatal): {e}")
            continue
        for t, d in re.findall(r"<item>.*?<title>(.*?)</title>.*?<pubDate>(.*?)</pubDate>", xml, re.S):
            title = _htmllib.unescape(re.sub(r"<!\[CDATA\[|\]\]>", "", t))
            title = re.sub(r"<[^>]+>", "", title)  # 제목 안 잔여 HTML 태그 제거 (agy 권고)
            title = re.sub(r"\s+", " ", re.sub(r"[\x00-\x1f\x7f]", " ", title)).strip()
            title = re.sub(r"\s+-\s+[^-]{2,40}$", "", title)
            # 헤드라인 속 금리 숫자(마케팅 스냅샷)는 GPT가 사실처럼 본문에 옮겨 적는 사고가
            # 실측됐다(E2E에서 'up to 4.10% APY' 누수). 숫자를 원천 제거해 누수 자체를 차단.
            # percent/per cent 철자 표기까지 마스킹 (codex).
            title = re.sub(r"\d+(?:\.\d+)?\s*(?:%|percent\b|per cent\b)", "…%", title, flags=re.I)
            if not (10 <= len(title) <= 140):
                continue
            try:
                pub = datetime.datetime.strptime(d.strip()[:16], "%a, %d %b %Y")
            except ValueError:
                continue
            if (now - pub).days > max_age_days:
                continue
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(title)
            if len(out) >= limit:
                return out
    return out


# === v8 explainer patterns (2026-05-23) ==========================
# Informational / comparison angles only — no fake "I tried X for 30 days" buyer-intent listicles.
TITLE_PATTERNS = [
    "How does a [thing] work?",
    "What is [thing] and how is it calculated?",
    "[Thing A] vs [Thing B]: which fits [situation]?",
    "How to compare [thing] without getting burned",
    "Is a [thing] worth it right now?",
    "Common mistakes with [thing] (and how to avoid them)",
    "How [thing] is taxed / what happens when rates change",
    "A beginner's guide to [thing]",
]
# v16: 실제로 쓰이던 제목 첫 단어가 목록에 없어 'other' 로 새던 구멍을 메운다
# ("Are Traditional CDs...", "Understanding the Advantages..." 가 둘 다 other 로 분류돼
#  다양성 카운트에서 빠졌고, 그 결과 forced hint 가 한 번도 발동하지 않았다 — 2026-08-16 실측).
PATTERN_PREFIXES = ["how", "what", "is", "are", "do", "does", "can", "when", "which", "why",
                    "should", "common", "a beginner", "the", "understanding"]
# 위 중 '질문형' 계열. 개별 prefix 만 세면 what↔how 를 번갈아 쓰는 것만으로 영구히 회피되므로
# 계열 단위 과점도 함께 감시한다.
QUESTION_PREFIXES = {"how", "what", "is", "are", "do", "does", "can", "when", "which", "why", "should"}
# 질문형이 과점일 때 강제할 서술형 구조 (제목 프롬프트의 패턴 3/6/7/8 과 1:1 대응)
_STATEMENT_HINTS = (
    "a direct '[Thing A] vs [Thing B]' comparison title",
    "a 'Common mistakes with ...' title",
    "a \"A beginner's guide to ...\" title",
    "a plain declarative title about how something is taxed, or about what changes when rates move",
)

STOPWORDS_TITLE = {
    "the","a","an","for","and","with","to","of","in","on","at","is","are","my","best","top","how","what",
    "your","this","that","its","it","be","by","or","as","you","not","do","does","worth","real","experience",
    "comparison","review","reviews","under","comparing","help","guide","tips","ultimate","cost","price",
    "prices","most","new","more","than","compare","which","when","where","who","why","ranked",
}


def _title_words(s):
    return [w.lower() for w in re.findall(r"[A-Za-z0-9']+", s) if w.lower() not in STOPWORDS_TITLE and len(w) > 2]


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    A, B = set(a), set(b)
    return len(A & B) / max(len(A | B), 1)


def _recent_keywords(used_topics, window=14, top_n=6):
    from collections import Counter
    bag = Counter()
    for t in used_topics[-window:]:
        for w in _title_words(t):
            bag[w] += 1
    return [w for w, _ in bag.most_common(top_n)]


def _pattern_of(title):
    s = title.lower().strip()
    if " vs " in s:
        return "vs"
    for p in PATTERN_PREFIXES:
        # 아포스트로피 형태도 같은 패턴 ("a beginner's guide to ..." → "a beginner")
        if s.startswith(p + " ") or s.startswith(p + "'") or s.startswith(p + "’"):
            return p
    return "other"


def _least_used_category(used_topics, categories, window=30):
    from collections import Counter
    counts = Counter()
    for t in used_topics[-window:]:
        slug = slugify(t)
        for c in categories:
            cw = c.replace("-", " ")
            if cw in t.lower() or c in slug:
                counts[c] += 1
                break
    sorted_cats = sorted(categories, key=lambda c: counts.get(c, 0))
    return random.choice(sorted_cats[:max(5, len(sorted_cats) // 3)])


def _forced_pattern_hint(used_topics, recent_n=6):
    """제목 형식이 한쪽으로 쏠렸을 때 프롬프트에 넣을 강제 지시문(str)을 반환. 없으면 None.

    v16(2026-08-16): 구버전은 개별 prefix 가 6편 중 4회 이상일 때만 발동해서, what/how 를
    번갈아 쓰는 것만으로 영구히 회피됐다(최근 20편 중 13편이 질문형인데 발동 0회 — 실측).
    ① 질문형 '계열' 과점을 먼저 보고 ② 그다음 개별 패턴 과점(임계 4→3)을 본다.
    """
    if len(used_topics) < recent_n:
        return None
    recent = used_topics[-recent_n:]
    prefixes = [_pattern_of(t) for t in recent]

    # ① 계열 과점 — 최근 제목이 거의 다 질문형이면 서술형을 강제한다.
    questions = sum(1 for p in prefixes if p in QUESTION_PREFIXES)
    if questions >= max(3, len(recent) - 2):
        return {
            "kind": "no_question",
            "avoid": None,
            "text": (
                f"FORCED FORM: {questions} of the last {len(recent)} titles were question-style, so THIS "
                "title MUST NOT be a question and MUST NOT start with a question word "
                "(How/What/Why/Is/Are/Do/Does/Can/When/Which/Should). Use "
                f"{random.choice(_STATEMENT_HINTS)}."
            ),
        }

    # ② 개별 패턴 과점 — 같은 첫 단어가 반복되면 다른 패턴으로 돌린다.
    most_common = max(set(prefixes), key=prefixes.count)
    if most_common != "other" and prefixes.count(most_common) >= 3:
        candidates = [p for p in PATTERN_PREFIXES if p != most_common]
        return {
            "kind": "prefix",
            "avoid": most_common,
            "text": (
                f"FORCED PATTERN: title MUST start with '{random.choice(candidates).title()}' "
                f"(the last {len(recent)} posts overused '{most_common.title()}')."
            ),
        }
    return None


# v12: 제목 클리셰 가드 — 사이트가 스스로 금지한 양산 단어가 제목으로 새던 구멍
_TITLE_CLICHES = ("unlock", "discover", "boost", "maximize", "secrets", "ultimate guide",
                  "essential guide", "game-changer", "revolutioniz")






# v14 (2026-07-28): 본문에 실제로 쓰는 계산기를 붙인다.
# 123편 전수 진단에서 "규칙 설명만 있고 독자가 자기 숫자로 판단할 방법이 없다"가 색인 거부의
# 핵심이었다. 계산기는 _includes/tools/ 에 있는 정적 JS 라 외부 호출·비용이 없다.
# v16(2026-08-16): 리드인 문장이 도구당 1개로 고정돼 있어, 같은 계산기가 붙은 글 7편에
# "Enter your own balance and APY below to see what the difference is worth over your time frame."
# 이 글자 하나 안 틀리고 반복됐다(실측) — 그 자체가 양산 지문. 도구별 변형 중 하나를 고른다.
_TOOL_RULES = (
    ("cd-penalty", (
        "penalt", "early withdrawal", "cash out", "break a cd", "breaking a cd", "withdraw early",
    ), (
        "Enter your CD's balance, rate, months held, and the penalty from your disclosure to see "
        "whether breaking it actually pays.",
        "Your own disclosure has the penalty terms — put them in below, with your balance and how "
        "long you have held the CD, and the math will show whether an early exit leaves you ahead.",
        "Rather than guess, run your numbers: balance, rate, months held, and the stated penalty.",
    )),
    ("ladder-builder", (
        "ladder", "laddering", "rungs",
    ), (
        "Put your total amount and the number of rungs in below to see each rung's size, maturity, "
        "and interest.",
        "How a ladder actually splits up depends on your total and how many rungs you want — set "
        "both below to see the maturity schedule.",
        "Try it with your own total: the rung sizes and maturity dates fall out of those two inputs.",
    )),
    ("apy-calculator", (
        "apy", "compound", "interest earn", "how much", "yield", "savings account", "money market",
        "returns", "earnings", "grow",
    ), (
        "Enter your own balance and APY below to see what the difference is worth over your time frame.",
        "The gap only means something against your own balance — put yours in below with the APY "
        "you are comparing.",
        "Run your own numbers instead: your balance, the APY on offer, and the period you plan to hold.",
        "Below, set the balance you would actually deposit and the rate you are being quoted.",
    )),
)


def _pick_tool(title, category):
    hay = f"{title} {category}".lower()
    for tool, keys, leads in _TOOL_RULES:
        if any(k in hay for k in keys):
            # leads 는 변형 튜플 (구버전 단일 문자열도 안전하게 허용)
            return tool, random.choice(leads) if isinstance(leads, (tuple, list)) else leads
    return None, None


def inject_tool(content, title, category):
    """주제에 맞는 계산기를 마지막 H2 직전에 삽입. 맞는 도구가 없으면 원본 그대로."""
    tool, lead = _pick_tool(title, category)
    if not tool:
        return content
    if "{% include tools/" in content:  # 이미 있으면 중복 삽입 금지
        return content
    block = f"\n{lead}\n\n{{% include tools/{tool}.html %}}\n"
    heads = list(re.finditer(r"\n##\s", content))
    if len(heads) >= 2:
        pos = heads[-1].start()
        return content[:pos] + block + content[pos:]
    return content.rstrip() + "\n" + block




# === v8 word count (2026-05-23) — quality over padding =============


# === v12 (2026-07-13) — 글별 구조 로테이션: 고정 8단 골격(전 글 동일 = 양산 지문) 제거 =====
_QUICK_LABELS = ["Quick answer", "Bottom line", "In short", "The short version"]
_MISTAKE_HEADINGS = ["Common Mistakes", "What People Get Wrong", "Pitfalls to Avoid", "Mistakes to Avoid"]
_FAQ_HEADINGS = ["Frequently Asked Questions", "FAQ", "Common Questions", "Questions Savers Ask"]


def _build_structure_plan():
    """글마다 다른 골격을 확률적으로 조립. 반환된 플랜 텍스트가 user 프롬프트에 그대로 들어간다."""
    parts = []
    if random.random() < 0.5:
        label = random.choice(_QUICK_LABELS)
        parts.append(
            f'- Open with ONE blockquote: "> **{label}:** <40-60 words: accurate direct answer to the title, '
            'with one general (non-fabricated) number or rule>." Then a blank line, then a 1-2 sentence specific lead.'
        )
    else:
        parts.append(
            "- NO opening blockquote. Open directly with a specific 2-3 sentence lead "
            "(a common mistake, a true general fact, or the core question) — no generic intro. "
            # v16: 5/7 편이 '상품 정의 → 많은 사람이 오해한다 → 이해하는 것이 essential 하다'
            # 3단 템플릿으로 시작했다(실측). 그 틀을 명시적으로 금지한다.
            "Do NOT open by defining the account type dictionary-style, and do NOT use the "
            "'many people underestimate/misunderstand X ... understanding X is essential/crucial' "
            "construction anywhere in the opening."
        )
    h2_count = random.randint(4, 8)
    q_share = random.choice(["one or two", "roughly half", "most"])
    parts.append(
        f"- {h2_count} H2 sections total; {q_share} of them phrased as real search questions, each followed "
        "immediately by a direct 40-60 word answer before expanding. The rest use plain descriptive headings."
    )
    if random.random() < 0.65:
        parts.append("- Include ONE Markdown comparison table (4+ rows, 3-4 columns) of stable, real attributes.")
    if random.random() < 0.45:
        parts.append(
            "- Include a practical checklist section readers can follow in order — write your own natural "
            "heading for it (do NOT title it 'How to Compare X Yourself')."
        )
    # v14: 실수/FAQ/워크드예시가 한 글에 동시에 붙어 'TL;DR+표+실수+FAQ' 4종 세트가
    # 91/123편에서 반복됐다(양산 지문). 셋 중 최대 1개만 붙이고 나머지는 금지한다.
    _extra = random.choice(["mistakes", "worked_example", "faq", "none"])
    if _extra == "mistakes":
        parts.append(
            f"- Include a '## {random.choice(_MISTAKE_HEADINGS)}' section: 3 accurate misconceptions, "
            "each with a one-line 'Why it matters:' explanation."
        )
    elif _extra == "worked_example":
        # v16: 구버전은 "labeled 'for example, if you had...'" 를 GPT 가 제목 지시로 읽어
        # '## For example, if you had $10,000 in a 12-month CD at 1.68% APY...' 라는 문장형 H2 를
        # 실제로 발행했다(2026-08-16 실측). 라벨은 본문 문장이고 제목은 명사구임을 못 박는다.
        parts.append(
            "- Work ONE clearly hypothetical numeric example into the body prose, introducing it inline "
            "with wording like \"for example, if you had...\", and walk through the arithmetic step by step. "
            "Put it under a SHORT descriptive noun-phrase heading — never use the example sentence itself "
            "as a heading, and never end a heading with '...'. "
            "If the example only credits interest once, call it simple interest — do not describe a single "
            "annual credit as compounding."
        )
    elif _extra == "faq":
        parts.append(f"- Near the end, include '## {random.choice(_FAQ_HEADINGS)}' with 3-5 ### Q&A pairs, accurate and specific.")
    if _extra != "faq":
        parts.append("- Do NOT add a FAQ or 'Questions' section to this article.")
    if _extra != "mistakes":
        parts.append("- Do NOT add a 'Common Mistakes' / 'What People Get Wrong' section to this article.")
    if _extra != "worked_example":
        parts.append("- Do NOT include a step-by-step worked numeric example section in this article.")
    parts.append(
        "- Close with a short conclusion and one concrete next step the reader can take today. "
        "Vary the closing style — do NOT open the final paragraph with 'In conclusion'."
    )
    return "\n".join(parts)




# 메타 디스크립션 양산 템플릿 단어 — 검출되면 재생성 (GPT가 프롬프트만으론 가끔 어김)
_BANNED_META = (
    "unlock", "discover", "boost", "maximize", "don't miss out", "dont miss out",
    "explore", "dive into", "learn everything", "in this guide", "find out how",
    "in our comprehensive guide", "the secrets",
)




# === v12 (2026-07-13) — 1차출처 실링크: '인용한다' 주장만 있고 외부 링크 0이던 모순 해소 ======
# 실존 확인(2026-07-13 curl 200)된 공식 URL만. GPT가 URL을 만들지 않도록 후처리에서만 링크.
_SOURCE_LINKS = [
    # v15: 전국 평균 금리를 인용하는 글은 그 수치의 출처 페이지로 직접 링크 (generic FDIC 링크보다 먼저 매칭)
    (r"FDIC(?:'s)? national[- ]average(?: deposit)? rates?|national[- ]average deposit rates?|National Rates and Rate Caps",
     "https://www.fdic.gov/national-rates-and-rate-caps"),
    (r"FDIC's BankFind( Suite)?|BankFind( Suite)?", "https://banks.data.fdic.gov/bankfind-suite/bankfind"),
    (r"FDIC", "https://www.fdic.gov/resources/deposit-insurance"),
    (r"Federal Reserve", "https://www.federalreserve.gov/monetarypolicy.htm"),
    (r"Consumer Financial Protection Bureau|CFPB", "https://www.consumerfinance.gov/"),
    (r"National Credit Union Administration|NCUA", "https://ncua.gov/consumers/share-insurance-coverage"),
    (r"U\.S\. Treasury", "https://www.treasurydirect.gov/"),
]

_MD_LINK_SPLIT = re.compile(r"(\[[^\]]*\]\([^)]*\)|!\[[^\]]*\]\([^)]*\))")


def _link_primary_sources(content, max_links=3, prefer_rates_page=False):
    """본문에서 1차출처 기관명 첫 언급을 공식 URL로 링크 (헤딩/기존 링크/이미지 제외).

    prefer_rates_page: FDIC 전국 평균 수치를 실제로 인용한 글이면 generic 'FDIC' 링크도
    수치의 출처인 국가금리 페이지로 보낸다 (E2E 실측 — GPT가 'FDIC national average' 정확
    문구를 안 써서 전용 패턴이 안 걸리고 generic FDIC만 걸리는 경우가 많았다)."""
    lines = content.split("\n")
    linked = 0
    used_urls = set()
    source_links = list(_SOURCE_LINKS)
    if prefer_rates_page:
        source_links = [(p, _FDIC_RATES_URL if u == "https://www.fdic.gov/resources/deposit-insurance" else u)
                        for p, u in source_links]
    for pattern, url in source_links:
        if linked >= max_links or url in used_urls:
            continue
        rx = re.compile(r"\b(" + pattern + r")\b")
        done = False
        for i, line in enumerate(lines):
            if done:
                break
            if line.lstrip().startswith("#") or line.lstrip().startswith("|"):
                continue  # 헤딩·표는 링크 안 넣음
            segments = _MD_LINK_SPLIT.split(line)
            for j, seg in enumerate(segments):
                if j % 2 == 1:  # 이미 마크다운 링크/이미지인 조각
                    continue
                m = rx.search(seg)
                if m:
                    segments[j] = seg[:m.start()] + f"[{m.group(1)}]({url})" + seg[m.end():]
                    lines[i] = "".join(segments)
                    linked += 1
                    used_urls.add(url)
                    done = True
                    break
    return "\n".join(lines)


_BARE_BRACKET = re.compile(r"\[([^\[\]\n]{10,120})\](?!\()")


def _resolve_bare_brackets(content, recent_posts):
    """v12b: GPT가 남긴 생 대괄호 [Title] 참조를 발행 전에 해소 — 실존 제목이면 실링크, 아니면 대괄호 제거."""
    title_map = {re.sub(r"\s+", " ", p["title"].replace("’", "'").strip().strip(".").lower()): p["url"]
                 for p in recent_posts if p.get("title") and p.get("url")}

    def repl(m):
        t = m.group(1)
        key = re.sub(r"\s+", " ", t.replace("’", "'").strip().strip(".").lower())
        if key in title_map:
            return f"[{t}]({title_map[key]})"
        if t[0].isupper() and len(t.split()) >= 3:
            return t  # 제목처럼 보이지만 매칭 없음 → 대괄호만 벗겨 깨진 마크업 방지
        return m.group(0)

    return _BARE_BRACKET.sub(repl, content)


# === v15 (2026-08-02) — 발행 전 결정적 품질 검증 + 수리 루프 (티스토리봇 P0-4 이식) ======
_BODY_CLICHES = (
    "in today's fast-paced world", "in the modern era", "have you ever wondered",
    "welcome to my blog", "let's dive in", "delve into", "delving into", "unlock the secrets",
    "embark on a journey", "treasure trove", "in the realm of", "tapestry of",
    "ever-evolving landscape", "navigate the world of", "it is important to note that",
    "it goes without saying", "needless to say",
)
_PROMISSORY = ("guaranteed returns", "risk-free profit", "risk-free returns", "you will earn")

# v15.1: 결정적 수리용 치환표 — GPT 재생성으로 못 잡은 문구를 코드로 직접 고쳐 발행한다
# (발행 스킵 금지 규칙). 의미 보존 + YMYL 안전 표현으로만 치환.
_CLICHE_FIXES = {
    "in today's fast-paced world": "today",
    "in the modern era": "today",
    "have you ever wondered": "many savers ask",
    "welcome to my blog": "",
    "let's dive in": "here is how it works",
    "delving into": "looking at",
    "delve into": "look at",
    "unlock the secrets": "understand the details",
    "embark on a journey": "get started",
    "treasure trove": "wealth",
    "in the realm of": "in",
    "tapestry of": "mix of",
    "ever-evolving landscape": "changing market",
    "navigate the world of": "understand",
    "it is important to note that": "note that",
    "it goes without saying": "clearly",
    "needless to say": "clearly",
}
_PROMISSORY_FIXES = {
    "guaranteed returns": "a fixed, contractual interest rate",
    "risk-free profit": "steady interest",
    "risk-free returns": "predictable interest",
    "you will earn": "you can expect to earn",
}


def _h2_lines(content):
    """fenced code block 밖에 있는 H2 만 (줄 인덱스, 제목 텍스트) 로 반환.

    codex(중간): 문서 전체에 정규식을 걸면 ``` 블록 안의 열 0 '## ...' 까지 헤딩으로
    오인한다. 검증과 수리가 같은 기준을 쓰도록 이 헬퍼 하나로 통일한다."""
    out = []
    fence = None
    for i, line in enumerate(content.split("\n")):
        stripped = line.strip()
        if fence:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            out.append((i, m.group(1)))
    return out


# 문장형 H2 를 제목 자리에 남겨야 할 때 쓰는 대체 제목 (API 없이 동작해야 한다)
_EXAMPLE_HEADINGS = ("Running the Numbers", "A Worked Example",
                     "Putting Numbers to It", "How the Math Works Out")


def _sentence_like_heading(h):
    """H2 텍스트가 '제목'이 아니라 '문장'인지 판정. 과탐으로 정상 글이 막히면 안 되므로
    명백한 신호만 본다 (실제 질문형 제목 'How Does X Work?' 은 반드시 통과해야 한다)."""
    s = h.strip().rstrip("#").strip()
    if not s:
        return False
    if s.endswith("...") or s.endswith("…"):
        return True
    if re.match(r"^(for example|for instance|if you|let'?s|suppose|imagine|say you)\b", s, re.I):
        return True
    # 물음표로 끝나는 진짜 질문형 제목은 길어도 정상
    if s.endswith("?"):
        return False
    # 마침표로 끝나면 문장 (약어 마침표는 제외)
    if s.endswith(".") and not re.search(r"\b(u\.s|inc|ltd|etc|vs|jr|sr)\.$", s, re.I):
        return True
    if len(s) > 80:
        return True
    return False


def _repair_normalize(content, market_data):
    """API 없이 도는 순수 문자열 수리 패스 — _deterministic_repair 본체이자, 분량 보강(API)
    이후 재정규화에도 재사용한다 (codex: 보강 섹션이 새 위반을 넣을 수 있음)."""

    def _sub_ci(text, bad, good):
        def _r(m):
            s = m.group(0)
            if good and s[:1].isupper():
                return good[0].upper() + good[1:]
            return good
        return re.sub(re.escape(bad), _r, text, flags=re.IGNORECASE)

    for bad, good in list(_CLICHE_FIXES.items()) + list(_PROMISSORY_FIXES.items()):
        if bad in content.lower():
            content = _sub_ci(content, bad, good)
    # 행 선두 들여쓰기(중첩 목록)는 보존 — 비선두 공백 연쇄만 축약 (codex)
    content = re.sub(r"(?<=\S)[ \t]{2,}", " ", content)

    content = re.sub(r"^#\s+.*\n?", "", content, flags=re.M)

    # v16: 문장형 H2 처리. 기본은 문단으로 강등하지만, 강등하면 정상 H2 가 3개 미만으로
    # 떨어지는 경우에는 강등 대신 짧은 제목으로 바꿔 끼운다 — codex(높음) 지적대로 강등이
    # H2 부족을 유발하면 API 보강에 의존하게 되고, 그 보강이 실패하면 발행 자체가 밀린다.
    # 이 경로는 OpenAI 없이도 동작해야 하므로 대체 제목은 로컬 상수에서 고른다.
    heads = _h2_lines(content)
    bad_heads = [(i, h) for i, h in heads if _sentence_like_heading(h)]
    if bad_heads:
        lines = content.split("\n")
        good = len(heads) - len(bad_heads)
        for i, h in bad_heads:
            if good >= 3:
                lines[i] = h  # 문장은 문단이 제자리
            else:
                lines[i] = "## " + random.choice(_EXAMPLE_HEADINGS)
                good += 1
        content = "\n".join(lines)

    content = re.sub(r"\n*^##\s+About the Author\b.*?(?=\n##\s|\Z)", "", content,
                     flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)

    # 미검증 소수점 2자리 금리 → 근사 표현. 근사 수식어가 이미 있거나 범위(-) 직후면
    # 'about' 생략 (codex: 'approximately about 4.2%' / '4.2%-about 4.8%' 방지)
    allowed = {r for _, r in (market_data or {}).get("rates", [])}

    def _round_rate(m):
        num = m.group(1)
        if num in allowed:
            return m.group(0)
        try:
            rounded = f"{round(float(num), 1):g}%"
        except ValueError:
            return m.group(0)
        prefix = m.string[max(0, m.start() - 16):m.start()].lower()
        bare = prefix.endswith(("about ", "approximately ", "around ", "roughly ", "~", "-", "–"))
        return rounded if bare else f"about {rounded}"

    return re.sub(r"\b(\d{1,2}\.\d{2})\s*%", _round_rate, content)


def _deterministic_repair(content, market_data, client=None, title=""):
    # client·title 인자는 호출부 호환용으로만 남긴다(2026-09-04 GPT 제거). 쓰지 않는다.
    """검증 실패 잔여 문제를 코드로 직접 수리 — '스킵 대신 발행' 규칙의 마지막 안전망.

    validate_post_quality 의 모든 검사 항목에 1:1 대응하는 기계적 수리:
    클리셰/약속성 문구 치환, H1·About 섹션 제거, 미검증 정밀 금리 근사화,
    FDIC 귀속 문구 삽입, 분량·H2 부족 시 섹션 보강."""
    content = _repair_normalize(content, market_data)

    # FDIC 수치 인용 귀속 강제 삽입 (전체 기준일 부재 또는 인용 근처 FDIC 부재 시)
    if market_data:
        cited = [r for _, r in market_data["rates"] if re.search(rf"\b{re.escape(r)}%", content)]
        if cited:
            first = re.search(rf"\b{re.escape(cited[0])}%", content)
            window = content[max(0, first.start() - 350):first.start() + 350]
            if market_data["as_of"] not in content or "fdic" not in window.lower():
                ins = f" (FDIC national average, as of {market_data['as_of']})"
                if ins not in content:
                    pos = first.end()
                    content = content[:pos] + ins + content[pos:]

    # 2026-09-04: 분량이 모자랄 때 GPT 로 문단을 늘리던 보강 루프를 걷어냈다(쿠마님 지시로
    # OpenAI 호출 전면 제거). 이제 분량은 글을 쓰는 사람이 채운다 — 모자라면
    # validate_post_quality 가 잡아 주고, write_manual_post.py 가 그 지적을 그대로 보여 준다.
    return content


def validate_post_quality(content, market_data=None):
    """발행 전 결정적(비확률) 품질 검증. 실패 사유 리스트 반환 — 빈 리스트면 통과.

    프롬프트 금지가 실출력에서 절반쯤 새는 문제(티스토리봇 실측)를 코드로 잡는다.
    검사는 전부 결정적 문자열/정규식 — 과탐으로 발행 0 되는 일이 없도록 명백한 것만."""
    problems = []
    text = content.lower()
    wc = len(content.split())
    if wc < 600:
        problems.append(f"body too short ({wc} words) — write a complete article")
    h2 = len(re.findall(r"^##\s", content, re.M))
    if h2 < 3:
        problems.append(f"only {h2} H2 sections — the structure plan requires more")
    hits = [c for c in _BODY_CLICHES if c in text]
    if hits:
        problems.append("banned AI-cliche phrase(s) used: " + ", ".join(hits[:3]))
    hits = [p for p in _PROMISSORY if p in text]
    if hits:
        problems.append("promissory phrasing used: " + ", ".join(hits))
    if re.search(r"^#\s", content, re.M):
        problems.append("markdown '# Title' line in body (title is rendered by the layout)")
    if re.search(r"^##\s+About the Author\b", content, re.M | re.I):
        problems.append("'About the Author' section in body (author box is rendered by the layout)")
    # v16: 문장이 통째로 H2 로 올라간 케이스 차단 (실측: '## For example, if you had $10,000
    # in a 12-month CD at 1.68% APY...' 가 라이브 목차에 그대로 노출됐다)
    bad_heads = [h for _, h in _h2_lines(content) if _sentence_like_heading(h)]
    if bad_heads:
        problems.append(
            "sentence used as an H2 heading: " + "; ".join(f'"{h[:60]}"' for h in bad_heads[:2])
            + " — headings must be short noun phrases or real questions, not example sentences"
        )
    if market_data:
        cited = [r for _, r in market_data["rates"] if re.search(rf"\b{re.escape(r)}%", content)]
        if cited:
            # codex: 월 이름만 있으면 통과하던 약한 검사 → 전체 기준일 존재 + 첫 인용 수치
            # 근처(±250자)에 FDIC 언급까지 요구. 문구 자체는 자유(템플릿화 방지, agy).
            if market_data["as_of"] not in content:
                problems.append(
                    f"FDIC number(s) {', '.join(cited[:3])} cited without the full as-of date "
                    f"('{market_data['as_of']}') anywhere in the article"
                )
            else:
                first = re.search(rf"\b{re.escape(cited[0])}%", content)
                window = content[max(0, first.start() - 350):first.start() + 350]
                if "fdic" not in window.lower():
                    problems.append(
                        f"FDIC number {cited[0]}% cited without attributing FDIC near the citation "
                        "(name the FDIC in the same passage)"
                    )
    # 소수점 2자리 % = '정밀한 현재 금리' 서술 스타일. 검증된 FDIC 수치가 아니면 출처 불명의
    # 금리 단정이므로 차단 (가설 예시는 4% / 4.5% 같은 라운드 숫자로 쓰게 유도).
    allowed = {r for _, r in (market_data or {}).get("rates", [])}
    precise = [p for p in re.findall(r"\b(\d{1,2}\.\d{2})\s*%", content) if p not in allowed]
    if precise:
        problems.append(
            "unverified precise rate(s) stated: " + ", ".join(sorted(set(precise))[:4])
            + "% — only numbers from the VERIFIED CURRENT DATA block may be that precise; "
            "use round numbers (e.g. 4%, 4.5%) for hypotheticals"
        )
    return problems




# 실행 진입점 없음 — 이 파일은 이제 "글을 만드는" 스크립트가 아니라 후처리 유틸리티 모음이다.
# 글은 클로드가 직접 쓰고 write_manual_post.py 가 이 모듈의 검증·링크·툴 삽입을 태워 _posts 에 넣는다.
#   python scripts/write_manual_post.py manual_posts.json


# v4_wordcount_patched
# v5_diversity_patched 2026-05-06
# v6_seo_patched 2026-05-08
# v7_pin_patched 2026-05-08
# v8_accuracy_rebuild 2026-05-23  (single niche HYSA/CD/MMA, no fabrication, 1st-party sources)
# v15_market_signals 2026-08-02  (real FDIC national-rate data + news-driven timely topics + quality validate/repair loop)
# v15.1_no_skip 2026-08-02  (never skip publishing: relaxed-retry + best-candidate topic fallback, deterministic content repair)
# v15.2_quality_floor 2026-08-02  (no-skip AND no-garbage: more retries, quality caps never relax; hard fails defer to the next cron slot)
# v15.3_no_extra_cost 2026-08-02  (dropped the gpt-4o escalation per owner cost rule — all calls stay on gpt-4o-mini)
# v16_pattern_rotation 2026-08-16  (title-pattern rotation actually fires: wider prefix list + question-family
#   over-use detection; per-tool lead-in variants; sentence-as-H2 blocked in validate + demoted in repair)
