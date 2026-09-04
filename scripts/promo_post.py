# -*- coding: utf-8 -*-
"""홍보 글 자동 생성 — 폐지됨 (2026-09-04).

이 스크립트는 gpt-4o-mini 로 홍보 글 본문을 통째로 만들던 경로였다. 쿠마님 지시로
영어 블로그에서 OpenAI 호출을 전부 걷어내면서 함께 내렸다.

대체 경로: 홍보 글도 클로드가 직접 쓰고 다른 글과 같은 파이프라인을 탄다.
  1) manual_posts.json 에 원고를 적는다 (date/title/category/description/tags/content)
  2) python scripts/write_manual_post.py manual_posts.json
     → 품질 검증 · 내부 링크 · 1차 출처 링크 · 툴 삽입 · 핀 이미지 · front matter · _posts 저장

홍보 글 관례(과거 이 파일이 지키던 것)
  · 제목·본문에 제품명을 억지로 반복하지 않는다.
  · 실제 링크를 넣는다(빈 CTA 금지).
  · 다른 글과 같은 분량·구조 기준을 그대로 적용한다.
"""
import sys

print(__doc__)
sys.exit(1)
