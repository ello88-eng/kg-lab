---
id: 2024-Xu-LargeLanguageModelsFor
title: "Large language models for cyber security: A systematic literature review"
authors: ["Xu, HanXiang", "Wang, ShenAo", "Li, Ningke", "Wang, Kailong", "Zhao, Yanjie", "Chen, Kai", "Yu, Ting", "Liu, Yang", "Wang, HaoYu"]
venue: "ACM Transactions on Software Engineering and Methodology"
year: 2024
doi: ""
url: ""
pdf: "raw_pdf/2024_HanXiang_LLM_for_CyberSecurity.pdf"
pdf_sha256: "13adbc6f60c9a0a4f9a068286e4a2c56b184494f914f346bb7e029def0b8ddb5"
tags: ["Large Language Model", "Cybersecurity", "Systematic Literature Review", "Software Vulnerability Detection", "Data Augmentation", "Hybrid Intelligence", "Autonomous Agents", "Security Engineering", "Threat Mitigation"]
free_tags: []
scores:
  overall: 3.50
bibtex: |
  @article{xu2024large,
    title={Large language models for cyber security: A systematic literature review},
    author={Xu, HanXiang and Wang, ShenAo and Li, Ningke and Wang, Kailong and Zhao, Yanjie and Chen, Kai and Yu, Ting and Liu, Yang and Wang, HaoYu},
    journal={ACM Transactions on Software Engineering and Methodology},
    year={2024},
    publisher={ACM New York, NY}
  }
---

## 🔑 키워드
Large Language Model, Cybersecurity, Systematic Literature Review, Software Vulnerability Detection, Data Augmentation, Hybrid Intelligence, Autonomous Agents, Security Engineering, Threat Mitigation

## 🧾 요약 (1문단)
이 논문 *“Large Language Models for Cyber Security: A Systematic Literature Review (2024)”*은 대형언어모델(LLM)의 보안 응용을 포괄적으로 조사한 체계적 문헌 리뷰(SLR)이다. 저자들은 47,135편의 논문 중 185편을 선별하여, 네 가지 연구질문(RQ)을 중심으로 분석하였다: (1) LLM이 적용된 보안 과제 유형, (2) 사용된 LLM 모델 아키텍처, (3) 보안 도메인 적응 기법(파인튜닝, 프롬프팅, 외부 증강 등), (4) 데이터 수집 및 전처리의 차이점이다. 결과적으로 LLM은 전통적인 취약점 탐지와 분석을 넘어, 자율적 취약점 수정(self-healing software) 및 데이터 생성 기반 보안 강화 등 새로운 패러다임을 제시한다. 특히 보안 연구에서 데이터 부족 문제를 생성적 증강(generative augmentation) 으로 해결하고, 정적 분석·퍼저(fuzzer)·검증기(verifier) 와 결합된 하이브리드 지능형 워크플로우가 효과적임을 강조하였다. 또한 다단계 보안 프로세스를 처리할 수 있는 자율형 LLM 에이전트가 차세대 보안 운영의 핵심으로 부상하고 있음을 지적하였다.결론적으로, LLM은 사이버보안의 분석 중심 접근에서 생성·수리 중심의 능동형 보안으로의 전환을 견인하고 있으며, 향후 연구는 LLM의 활용과 자체 보안성 확보 간의 균형이 핵심 과제로 제시된다.

## 🧭 자체 평가 메모
강점: 방대한 문헌(47K→185편)에 기반한 체계적 분석으로, LLM과 사이버보안의 교차점을 종합적으로 조망함. RQ별 구분이 명확하고, 데이터 증강·하이브리드 워크플로우·자율 에이전트 등 최신 경향을 포착함.한계/열린점: 정량적 메타분석보다는 서술적 요약에 치중하였으며, 모델 성능 비교나 데이터셋 표준화 논의는 부족함. 실제 운영 환경에서의 LLM 기반 보안 적용사례 및 위협 모델링(예: prompt injection, data leakage)에 대한 실증 분석이 제한적임.비평: “LLM4Sec”을 포괄적 프레임워크로 제시했지만, 향후 연구는 LLM 자체 보안성(self-audit, secure reasoning)과 모자이크형 위협 탐지 같은 복합적 상호작용 분석으로 확장될 필요가 있음.
