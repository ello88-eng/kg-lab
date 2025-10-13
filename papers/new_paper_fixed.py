#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_paper.py - Single-file CLI
- Pick a PDF from papers/raw_pdf (auto if only one; otherwise interactive or via --pdf)
- Paste BibTeX from Google Scholar (multi-line; end with a blank line)
- Parse metadata from BibTeX (title, authors, year, venue/journal, doi/url)
- Ask only for keywords, 1-paragraph summary, overall score, optional comment
- Create Markdown note with YAML front matter
- Update index/papers.csv and index/papers.jsonl
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ---------- Paths ----------
ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw_pdf"
NOTES_DIR = ROOT / "notes"
INDEX_DIR = ROOT / "index"
ASSETS_DIR = ROOT / "assets"
CSV_FP = INDEX_DIR / "papers.csv"
JSONL_FP = INDEX_DIR / "papers.jsonl"

CSV_HEADERS = ["id", "title", "year", "venue", "overall", "tags", "authors", "pdf"]

NOTE_TEMPLATE = """---
id: {id}
title: "{title}"
authors: {authors_json}
venue: "{venue}"
year: {year}
doi: "{doi}"
url: "{url}"
pdf: "{pdf_rel}"
pdf_sha256: "{pdf_sha256}"
tags: {tags_json}
free_tags: []
scores:
  overall: {overall}
bibtex: |
{bibtex_indented}
---

## 🔑 키워드
{keywords}

## 🧾 요약 (1문단)
{summary}

## 🧭 자체 평가 메모
{comment}
"""

# ---------- Utils ----------
def ensure_dirs():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def compute_sha256(fp: Path) -> str:
    h = hashlib.sha256()
    with fp.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_multiline(prompt: str) -> str:
    print(prompt)
    print("(빈 줄에서 Enter를 누르면 입력이 종료됩니다.)")
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()

def _clean(s: str) -> str:
    return s.strip() if s else ""

def slugify_title(title: str, max_words: int = 4) -> str:
    """Make a compact slug from title (keep letters/digits across locales)."""
    if not title:
        return "untitled"
    # Normalize, replace separators with space
    s = unicodedata.normalize("NFKD", title)
    s = re.sub(r"[^\w\s-]", " ", s, flags=re.UNICODE)
    s = re.sub(r"[\s_-]+", " ", s, flags=re.UNICODE).strip()
    words = s.split()
    words = words[:max_words]
    # Join words without spaces; capitalize first letter of each word
    return "".join(w[:20].capitalize() for w in words) or "untitled"

def family_name_from_author(a: str) -> str:
    """Extract family name from 'Last, First' or 'First Middle Last' style."""
    a = a.strip()
    if not a:
        return "Anon"
    if "," in a:
        return a.split(",", 1)[0].strip().replace(" ", "")
    parts = a.split()
    return parts[-1]

def parse_bibtex(bib: str) -> Dict[str, Any]:
    """Robust-enough BibTeX parser for common fields (regex-based; no deps)."""
    def rex(field: str) -> re.Pattern:
        # matches: field = { ... } or " ... "
        return re.compile(rf"{field}\s*=\s*(\{{(?P<brace>.*?)\}}|\"(?P<quote>.*?)\")", re.IGNORECASE | re.DOTALL)
    def get(field: str) -> str:
        m = rex(field).search(bib)
        if not m:
            return ""
        return _clean(m.group("brace") or m.group("quote") or "")
    title = get("title")
    authors_raw = get("author")
    authors_list = [a.strip() for a in re.split(r"\s+and\s+", authors_raw, flags=re.IGNORECASE) if a.strip()]
    year = get("year")
    venue = get("booktitle") or get("journal")
    doi = get("doi")
    url = get("url")
    key_match = re.search(r"@\w+\s*\{\s*([^,\s]+)", bib)
    key = key_match.group(1) if key_match else ""
    return dict(title=title, authors=authors_list, year=year, venue=venue, doi=doi, url=url, key=key)

def load_csv_map() -> Dict[str, Dict[str, str]]:
    if not CSV_FP.exists():
        return {}
    rows = {}
    with CSV_FP.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows[r["id"]] = r
    return rows

def save_csv_map(rows: Dict[str, Dict[str, str]]):
    with CSV_FP.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for _, r in sorted(rows.items(), key=lambda x: x[0]):
            writer.writerow(r)

def load_jsonl_map() -> Dict[str, Dict[str, Any]]:
    data = {}
    if not JSONL_FP.exists():
        return data
    with JSONL_FP.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "id" in obj:
                    data[obj["id"]] = obj
            except JSONDecodeError:
                continue
    return data

def save_jsonl_map(objmap: Dict[str, Dict[str, Any]]):
    with JSONL_FP.open("w", encoding="utf-8") as f:
        for _, obj in sorted(objmap.items(), key=lambda x: x[0]):
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def prompt_optional(msg: str, default: str = "") -> str:
    val = input(f"{msg}{f' [{default}]' if default else ''}: ").strip()
    return val if val else default

def prompt_score(msg: str, default: float = 4.0) -> float:
    while True:
        raw = input(f"{msg} (0~5){f' [{default}]' if default is not None else ''}: ").strip()
        if not raw and default is not None:
            return float(default)
        try:
            s = float(raw)
            if 0.0 <= s <= 5.0:
                return s
        except ValueError:
            pass
        print("  → 숫자(0~5)를 입력해주세요.")

def make_id(year: str, first_author: str, title: str) -> str:
    y = year if year and year.isdigit() else "YYYY"
    fa = re.sub(r"[^A-Za-z0-9가-힣]", "", family_name_from_author(first_author)) or "Anon"
    slug = slugify_title(title)
    return f"{y}-{fa}-{slug}"

def unique_note_path(base_id: str) -> Tuple[str, Path]:
    """Ensure unique note path; add suffix -2, -3 if needed."""
    pid = base_id
    note_fp = NOTES_DIR / f"{pid}.md"
    n = 2
    while note_fp.exists():
        pid = f"{base_id}-{n}"
        note_fp = NOTES_DIR / f"{pid}.md"
        n += 1
    return pid, note_fp

def indent_block(text: str, spaces: int = 2) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else pad for line in text.splitlines())

def pick_pdf_interactive() -> Path:
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"raw_pdf 폴더에 PDF가 없습니다: {RAW_DIR}")
    if len(pdfs) == 1:
        return pdfs[0]
    print("처리할 PDF를 선택하세요:")
    for i, p in enumerate(pdfs, 1):
        print(f"  {i}. {p.name}")
    while True:
        sel = input(f"번호(1~{len(pdfs)}) 입력: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(pdfs):
            return pdfs[int(sel)-1]
        print("  → 올바른 번호를 입력하세요.")

# ---------- Main workflow ----------
def create_note_and_indexes(pdf_path: Path):
    ensure_dirs()
    if not pdf_path.exists():
        raise SystemExit(f"PDF가 존재하지 않습니다: {pdf_path}")

    # 1) BibTeX paste
    bibtex = read_multiline("\n📑 Google Scholar에서 BibTeX을 복사하여 붙여넣으세요.")
    if not bibtex:
        print("BibTeX가 비어 있습니다. 종료합니다.")
        sys.exit(1)

    meta = parse_bibtex(bibtex)
    title = meta.get("title", "")
    authors: List[str] = meta.get("authors", [])
    year = meta.get("year", "")
    venue = meta.get("venue", "")
    doi = meta.get("doi", "")
    url = meta.get("url", "")

    if not title:
        print("⚠️  BibTeX에서 title을 찾지 못했습니다. 수동으로 입력하세요.")
        title = prompt_optional("논문 제목", "Untitled")
    if not authors:
        print("⚠️  BibTeX에서 author를 찾지 못했습니다. 수동으로 입력하세요. (쉼표 또는 and 구분)")
        ar = prompt_optional("저자들", "")
        authors = [a.strip() for a in re.split(r"[;,]| and ", ar, flags=re.IGNORECASE) if a.strip()] or ["Anon"]
    if not year:
        year = prompt_optional("연도 (예: 2023)", "")
    if not venue:
        venue = prompt_optional("게재(venue/journal)", "")

    # 2) Minimal user inputs
    keywords = prompt_optional("🔑 키워드(콤마로 구분)", "")
    summary = prompt_optional("🧾 1문단 요약", "")
    comment = prompt_optional("💬 코멘트(선택)", "")
    overall = prompt_score("⭐ 전체 점수", 4.0)

    # 3) Build IDs and paths
    first_author = authors[0] if authors else "Anon"
    base_id = make_id(year, first_author, title)
    paper_id, note_fp = unique_note_path(base_id)

    pdf_sha256 = compute_sha256(pdf_path)
    pdf_rel = str(pdf_path.relative_to(ROOT)).replace("\\", "/")
    tags = [t.strip() for t in keywords.replace(";", ",").split(",") if t.strip()]

    # 4) Write note
    bibtex_indented = indent_block(bibtex, 2)
    note_text = NOTE_TEMPLATE.format(
        id=paper_id,
        title=title.replace('"', '\"'),
        authors_json=json.dumps(authors, ensure_ascii=False),
        venue=venue,
        year=year if year else "null",
        doi=doi,
        url=url,
        pdf_rel=pdf_rel,
        pdf_sha256=pdf_sha256,
        tags_json=json.dumps(tags, ensure_ascii=False),
        overall=f"{overall:.2f}",
        bibtex_indented=bibtex_indented,
        keywords=keywords,
        summary=summary,
        comment=comment,
    )
    note_fp.write_text(note_text, encoding="utf-8")
    print(f"📝 노트 저장: {note_fp}")

    # 5) Update CSV (upsert)
    csv_map = load_csv_map()
    csv_map[paper_id] = {
        "id": paper_id,
        "title": title,
        "year": str(year),
        "venue": venue,
        "overall": f"{overall:.2f}",
        "tags": ";".join(tags),
        "authors": ";".join(authors),
        "pdf": pdf_rel,
    }
    save_csv_map(csv_map)
    print(f"📇 CSV 업데이트: {CSV_FP}")

    # 6) Update JSONL (upsert)
    jsonl_map = load_jsonl_map()
    jsonl_map[paper_id] = {
        "id": paper_id,
        "title": title,
        "year": int(year) if str(year).isdigit() else year,
        "venue": venue,
        "scores": {"overall": overall},
        "tags": tags,
        "authors": authors,
        "path": str(note_fp.relative_to(ROOT)).replace("\\", "/"),
        "pdf": pdf_rel,
        "pdf_sha256": pdf_sha256,
        "keywords": keywords,
        "summary": summary[:2000],
        "doi": doi,
        "url": url,
        "bibtex_key": meta.get("key", ""),
    }
    save_jsonl_map(jsonl_map)
    print(f"🧾 JSONL 업데이트: {JSONL_FP}")

    print("\n✅ 완료! 다음 명령으로 노트 확인 가능:")
    print(f"   code {note_fp}  # 또는 에디터로 열기")

def main():
    parser = argparse.ArgumentParser(description="PDF→BibTeX 기반 노트 생성 & 인덱스 업데이트 (단일 파일)")
    parser.add_argument("--pdf", type=str, default="", help="처리할 PDF 경로 (없으면 raw_pdf에서 선택)")
    args = parser.parse_args()

    ensure_dirs()

    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            raise SystemExit(f"PDF가 존재하지 않습니다: {pdf_path}")
    else:
        # Auto-pick: if one file, pick it; else interactive selection
        pdf_path = pick_pdf_interactive()

    create_note_and_indexes(pdf_path)

if __name__ == "__main__":
    main()
