---
id: 2023-Andrew-KnowledgeGraphsForCybersecurity-2
title: "Knowledge graphs for cybersecurity: a framework for honeypot data analysis"
authors: ["Andrew, Yevonnael", "Lim, Charles", "Budiarto, Eka"]
venue: "2023 IEEE International Conference on Cryptography, Informatics, and Cybersecurity (ICoCICs)"
year: 2023
doi: ""
url: ""
pdf: "raw_pdf/2023_Yevonnael_Kg_for_CyberSecurity.pdf"
pdf_sha256: "f1d32f9441ee5a7d3ab574cd74a41634adffde3f7f920a11f1c48612f9ae14bc"
tags: ["Honeypot", "Knowledge Graph", "Cyber Threat Intelligence", "Neo4j", "Data Integration / Reasoning", "Cyberattack Pattern Analysis"]
free_tags: []
scores:
  overall: 4.30
bibtex: |
  @inproceedings{andrew2023knowledge,
    title={Knowledge graphs for cybersecurity: a framework for honeypot data analysis},
    author={Andrew, Yevonnael and Lim, Charles and Budiarto, Eka},
    booktitle={2023 IEEE International Conference on Cryptography, Informatics, and Cybersecurity (ICoCICs)},
    pages={275--280},
    year={2023},
    organization={IEEE}
  }
---

## 🔑 키워드
Honeypot, Knowledge Graph, Cyber Threat Intelligence, Neo4j, Data Integration / Reasoning, Cyberattack Pattern Analysis

## 🧾 요약 (1문단)
본 논문은 사이버보안 분야에서 발생하는 복잡하고 다양한 데이터를 효율적으로 분석하기 위해 **지식그래프(Knowledge Graph)**를 활용하는 방법을 제시한다. 저자들은 Cowrie와 Dionaea와 같은 honeypot에서 수집된 공격 로그를 표준화·전처리한 뒤 MongoDB에 저장하고, 이를 Neo4j 기반 지식그래프로 변환하였다. IP 주소, 공격 명령, 세션, 사용자 인증정보 등을 노드로, 이들 간 관계(예: ORIGINATED_FROM, EXECUTED, NEXT)를 엣지로 구성함으로써 공격 행위의 순서 및 연관성을 탐색할 수 있게 하였다. 또한 AbuseIPDB와 ip-api 등의 외부 데이터와 연결하여 IP 평판 및 위치 정보를 추가함으로써 분석의 풍부성을 높였다. 결과적으로, 특정 세션 내 명령 패턴 분석, IP별 공격 활동 요약, 지리적 공격 분포 등 다양한 쿼리를 통해 공격 행위의 맥락적 이해와 위협 탐지 효율을 크게 향상시킬 수 있음을 보였다. 저자들은 향후 연구 방향으로 실시간 그래프 업데이트, 머신러닝 기반 패턴 인식, 공격 예측 및 행위자 식별을 제안하였다.

## 🧭 자체 평가 메모
이 논문의 강점은 실제 honeypot 로그를 이용해 Neo4j 기반의 지식그래프를 완성한 실용적 사례를 제시했다는 점에 있다. Cypher 쿼리 예시를 통해 구체적인 분석 시나리오를 제시하였으며, AbuseIPDB와 ip-api 등 외부 위협정보를 통합하여 실증적 가치를 높였다. 또한 honeypot 데이터를 Cyber Threat Intelligence(KG Type II)로 구조화하는 명확한 프레임워크를 제시한 점도 돋보인다. 반면 한계로는 시스템의 성능 및 확장성 평가가 정량적으로 부족하며, 자동화된 엔티티 추출(NER/NLP)이나 지식 추론(reasoning) 적용이 개념적 수준에 머물러 있다. 다양한 honeypot 포맷에 대한 범용성 검증이 이루어지지 않아 MongoDB 스키마에 강하게 의존하고 있으며, 실시간 스트리밍 데이터 처리나 공격 예측 모델과의 연동 역시 향후 과제로 남는다.이 논문은 **“데이터-행위 관계를 그래프화하여 분석한다”**는 점에서 매우 유용한 토대이지만,
