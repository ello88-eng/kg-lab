# 🧠 Research Paper Knowledge Base

이 폴더는 내가 읽은 논문들을 **체계적으로 정리·검색·활용**하기 위한 개인 지식 베이스입니다.  
각 논문은 **메타데이터(YAML Front Matter)** + **1문단 요약 + 평가 + 후속 아이디어** 형태로 관리되며,  
향후 지식 그래프(KG), 검색 인덱스, Mosaic Effect / 데이터 유출 리스크 분석 등에 활용됩니다.

---

## 📂 폴더 구조

```
papers/
  raw_pdf/                 # 논문 PDF 원본 (SHA-256 기반 무결성 관리 가능)
  notes/                   # 논문별 마크다운 노트 (요약 + 평가 + bibtex)
  assets/                  # 캡처 이미지 및 도표 저장
  index/
    papers.csv             # 간략 인덱스 (표 형태: id, title, tags, score 등)
    papers.jsonl           # 상세 인덱스 (머신용 검색/임베딩 입력)
    tags.yml               # 표준 태그 목록 (Controlled Vocabulary)
  README.md                # 현재 파일
```

---

## 🗂 파일명 규칙

| 타입 | 형식 | 예시 |
|------|------|------|
| PDF | `YYYY-FirstAuthor-Slug.pdf` | `2023-Zeng-BoustrophedonCPP.pdf` |
| Note | `YYYY-FirstAuthor-Slug.md` | `2023-Zeng-BoustrophedonCPP.md` |
| Asset | `Slug-fig1.png` | `2023-Zeng-BoustrophedonCPP-fig2.png` |

> **슬러그(Slug)**: 논문 주제 요약 (공백 없이 짧게, 예: `BoustrophedonCPP`, `GraphVRP` 등)

---

## 🧾 논문 노트 템플릿 (`notes/*.md`)

각 논문 노트는 YAML Front Matter와 본문을 포함합니다:

```markdown
---
id: 2023-Zeng-BoustrophedonCPP
title: "Adaptive Boustrophedon Coverage for Fixed-Wing UAVs"
authors: ["Zeng, A.", "Kim, T.", "Yoon, S."]
venue: "IJCAS"
year: 2023
pdf: "../raw_pdf/2023-Zeng-BoustrophedonCPP.pdf"
tags: ["CPP","FixedWing","Boustrophedon","MultiAgent"]
free_tags: ["line-spacing=164m","altitude-separation"]
scores:
  novelty: 4.5
  rigor: 3.5
  relevance: 5.0
  clarity: 4.0
  reproducibility: 3.0
  engineering: 3.5
overall: 4.15
bibtex: |
  @inproceedings{zeng2023adaptive,
    title={Adaptive Boustrophedon Coverage for Fixed-Wing UAVs},
    author={Zeng, A. and Kim, T. and Yoon, S.},
    booktitle={IJCAS},
    year={2023}
  }
---

## 🔑 키워드
CPP, fixed-wing, boustrophedon, line spacing, overlap penalty

## 🧾 요약
본 논문은 고정익 UAV의 선회 제약을 고려한 boustrophedon 경로를 제안한다. ...

## 📌 핵심 기여
- PCA 기반 라인 정렬 + 장애물 패널티
- 커버리지 향상, 경로 중복 감소

## 🧪 실험/결과
- 맵 12종, UAV 4~12대
- 기존 대비 커버리지 +3~5%p

## 🧭 자체 평가/메모
- SA+Greedy 워밍 스타트와 궁합 좋음
- Line spacing 자동화 확장 가능

## 📝 To-Do
- [ ] 우리 데이터셋 실험 복제
- [ ] Altitude → MinOnlyBounds 적용
```

---

## 🧮 평가 스코어 정의

| 항목 | 의미 | 범위 | 기본 가중치 |
|------|------|------|-------------|
| novelty | 연구의 새로움 | 0–5 | 0.25 |
| rigor | 이론적 엄밀성 | 0–5 | 0.20 |
| relevance | 내 프로젝트와의 연관성 | 0–5 | 0.25 |
| clarity | 설명/구조의 명확성 | 0–5 | 0.10 |
| reproducibility | 재현성/공개성 | 0–5 | 0.10 |
| engineering | 실무·시스템 적용성 | 0–5 | 0.10 |
| overall | 가중 평균 | 0–5 | 자동 계산 |

---

## 🏷 태그 관리

- 표준 태그는 `index/tags.yml`에서 관리 (Controlled Vocabulary)
- 자유 태그(`free_tags`)는 임시 용도로 사용 후 표준화
- 예시:

```yaml
# tags.yml
topics:
  - CPP
  - MultiAgent
  - VRP
  - Diffusion
  - DataFactory
methods:
  - Heuristic
  - RL
  - GraphCut
  - SA
domains:
  - Aerial
  - Satellite
  - Robotics
```

---

## 🔍 인덱스 파일

- `index/papers.csv`  
  논문 개요를 간단히 필터링/정렬용으로 관리

```
id,title,year,venue,overall,tags,authors
2023-Zeng-BoustrophedonCPP,Adaptive Boustrophedon Coverage for Fixed-Wing UAVs,2023,IJCAS,4.15,"CPP;FixedWing;Boustrophedon","Zeng;Kim;Yoon"
```

- `index/papers.jsonl`  
  향후 임베딩/검색/지식그래프 입력용 (1 line = 1 paper JSON)

---

## ⚙️ 운영 가이드

1. **새 논문 추가**
   - PDF 저장 → SHA-256 계산 (선택)
   - 템플릿 복사 후 요약/스코어 작성
   - `index/papers.csv` 및 `papers.jsonl`에 추가

2. **태그 통일**
   - 기존 `tags.yml` 내 항목을 우선 사용
   - 새로운 태그는 `free_tags`로 임시 추가 후 주기적 정리

3. **평가 스크립트(선택)**
   - `overall = Σ(score × weight)` 자동계산 가능  
     → 향후 Python 스크립트로 제공 예정

4. **백업 및 버전관리**
   - `git`으로 버전 관리  
   - PDF는 `.gitignore`에 추가 가능 (SHA-256만 추적)

---

## 🔭 향후 확장 계획

| 목표 | 설명 |
|------|------|
| 🔹 Knowledge Graph | `notes/`의 YAML 메타데이터 + 요약 문단에서 엔티티/관계 추출 |
| 🔹 검색 인덱스 | `papers.jsonl` 기반 SentenceTransformer + FAISS |
| 🔹 리스크 분석 | Mosaic Effect / DLP 감지 실험에 논문 메타 활용 |
| 🔹 시각화 | Neo4j, Gephi 또는 Streamlit 대시보드로 확장 |

---

**작성자:** 개인 연구용 Paper Knowledge Base  
**버전:** 0.1 (초기 세팅)
