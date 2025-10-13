---
id: 2024-Cao-AFrameworkForPrivacy
title: "A Framework for Privacy-Preserving Efficient Collaborative Learning"
authors: ["Cao, Jianxiang", "Song, Xing", "Shang, Wenqian"]
venue: "2024 IEEE International Conferences on Internet of Things (iThings) and IEEE Green Computing \& Communications (GreenCom) and IEEE Cyber, Physical \& Social Computing (CPSCom) and IEEE Smart Data (SmartData) and IEEE Congress on Cybermatics"
year: 2024
doi: ""
url: ""
pdf: "raw_pdf/2024_Jianxian_FrameworkPrivacy-Preserving.pdf"
pdf_sha256: "4a9ca1eb66d9dc3f3fa49b4ef2b04c140ad2330706c8ff28bce0a5efb819aecd"
tags: ["Federated Learning(FL)", "EPPCL(Efficient Privacy-Preserving Collaborative Learning)", "CP-ABE(Ciphertext-Policy Attribute-Based Encryption)", "지식 증류(global→local)", "데이터 권한 부여/암·복호화", "Non-IID 데이터", "IoT", "중앙 서버 집계."]
free_tags: []
scores:
  overall: 4.00
bibtex: |
  @inproceedings{cao2024framework,
    title={A Framework for Privacy-Preserving Efficient Collaborative Learning},
    author={Cao, Jianxiang and Song, Xing and Shang, Wenqian},
    booktitle={2024 IEEE International Conferences on Internet of Things (iThings) and IEEE Green Computing \& Communications (GreenCom) and IEEE Cyber, Physical \& Social Computing (CPSCom) and IEEE Smart Data (SmartData) and IEEE Congress on Cybermatics},
    pages={241--245},
    year={2024},
    organization={IEEE}
  }
---

## 🔑 키워드
Federated Learning(FL), EPPCL(Efficient Privacy-Preserving Collaborative Learning), CP-ABE(Ciphertext-Policy Attribute-Based Encryption), 지식 증류(global→local), 데이터 권한 부여/암·복호화, Non-IID 데이터, IoT, 중앙 서버 집계.

## 🧾 요약 (1문단)
저자는 데이터 소유권과 사용권을 분리하는 **3계층 프레임워크(EPPCL)**를 제안합니다: (1) 수집 계층에서 소유자가 데이터를 업로드, (2) CP-ABE로 접근 정책을 암호문에 내장하고 기관의 속성 권한기관(AA)이 키를 발급·관리, (3) 훈련 계층에서 트레이너가 복호화로 얻은 인가 데이터로 훈련합니다. 학습은 개선된 FL을 사용해, 매 라운드 글로벌 모델을 teacher, 로컬 모델을 student로 두고 로컬 지식 증류 → 로컬 학습을 순차 수행한 뒤 중앙에서 가중 평균으로 집계합니다. 실험에서는 CP-ABE 암·복호화 시간이 속성 수와 데이터 크기에 대해 대체로 선형적으로 증가하고, CIFAR-10/CINIC-10/MNIST에서 FedAvg 대비 정확도 상승, 특히 Non-IID 분포에서 이점이 큽니다.

## 🧭 자체 평가 메모
강점: 권한 부여/훈련을 한 프레임으로 결합(소유권-사용권 분리), Non-IID 대응을 위한 글로벌→로컬 지식 증류가 단순하면서 효과적, 시스템 관점(AA/클라우드/트레이너)과 학습 관점을 함께 제시.한계/열린 점: 트레이너가 평문 데이터에 접근하는 구조라(복호화 후) 모델 업데이트 보호(예: secure aggregation, DP)나 모델 인퍼런스 유출 방어는 미포함. FedProx/SCAFFOLD/FedOpt 같은 Non-IID 강건 베이스라인이나 DP-FL/HE 대비도 없음. 증류-학습 구간 비율(예: 8:2, 7:3)의 민감도 분석과 통신/연산 오버헤드 보고가 제한적. 실제 정책 충돌/키 관리 운영 시나리오가 더 필요.확장 아이디어: (i) AA 신뢰 최소화(예: 다자키 관리/키 분산), (ii) secure aggregation + DP 결합으로 모델/업데이트 보호, (iii) 텍스트·시계열 등 타 도메인 검증, (iv) 증류 데이터 선택·온톨로지 태깅으로 KG와 연계해 실험 메타데이터를 관리.
