## 📂 1. 개인 프로젝트 (ETL 자동화 시스템)


---

### 🔹 프로젝트 개요

- **목표**: ETL 원리를 활용해 정해진 시간마다 데이터 수집 → 변환 → 적재를 자동화
- **역할**: 프로젝트 리더 (개인 프로젝트)
- **주요 기능**
    - `crontab` 스케줄러로 정기 실행
    - MySQL DB에서 원본 데이터 추출
    - 가공(혈당/심박 데이터 집계, 기간별 AM/PM 구분)
    - 적재 테이블에 저장

---

### 🔹 데이터 파이프라인 (ETL 구조)

1. **Extract**
    - DB(MySQL)에서 `혈당(fmd_trend_analysis_blood_glucose)` / `심박수(fmd_trend_analysis_heart_rate)` 데이터 추출
2. **Transform**
    - `date`, `period(AM/PM)` 생성
    - 일별 평균 혈당/심박 조인
    - 일자 기준으로 정렬
3. **Load**
    - 가공된 데이터를 DB2(MySQL)의 `fmd_trend_analysis_combined_data` 테이블에 삽입
    - `last_run_date.txt` 활용하여 중복/누락 방지
4. **Schedule**
    - `crontab.sh` → Python ETL 스크립트 실행 (가상환경 자동 로드)

---

### 🔹 기술 스택

- Python, Pandas, SQLAlchemy, PyMySQL
- MySQL
- FastAPI(추가 연계 가능 구조)
- Crontab (자동화)

---

### 🔹 성과 및 특징

- 완전 자동화된 **데이터 적재 시스템** 구축
- ETL 프로세스 단위 테스트 및 예외처리 적용
- 팀 프로젝트 기반 활용 가능 (ML 프로젝트와 연동 가능)

---

## 📂 2. 팀 프로젝트 (ML – 기업 성공 확률 예측)


---

### 🔹 프로젝트 개요

- **목표**: 기업 정보 및 재무 데이터를 기반으로 **기업 성공 확률(0~1)** 예측 모델 개발
- **데이터 출처**: [Dacon **기업 성공 확률 예측 해커톤: 미래의 성공기업을 발굴하라!**](https://www.dacon.io/competitions/official/236475/data)

---

### 🔹 데이터 처리

- **원본 데이터**: train.csv (4376개 기업, 14개 컬럼)
- **전처리 과정**
    - 결측치 제거 → 2578개 기업 데이터 확보
    - object → float 변환 (기업 가치 범위 → 평균값)
    - object → int 변환 (인수 여부, 상장 여부 → 1/0)
    - 투자 단계 (Seed, Series A~C, IPO) → 로그 스케일링 적용

---

### 🔹 모델링 과정

1. **데이터 그룹화**
    - 기준: `Country`, `Industry` (국가 + 산업 분야별 회귀모델 학습)
2. **특성 선택**
    - 종속변수(성공 확률)와 **상관계수 |0.3| 이상** 변수만 feature로 선택
3. **데이터 분할**
    - 학습:검증 = 8:2, Seed=10
4. **사용 모델**
    - DecisionTreeRegressor
    - RandomForestRegressor
    - LinearRegression
5. **평가 지표**
    - MAE (평균 절대 오차)
    - MSE (평균 제곱 오차)
    - RMSE (제곱 평균 제곱근 오차)

---

### 🔹 모델 성능 비교 (Validation 기준)

| 모델 | MAE | MSE | RMSE |
| --- | --- | --- | --- |
| DecisionTreeRegressor | 0.242 | 0.096 | 0.310 |
| RandomForestRegressor | 0.204 | 0.063 | 0.250 |
| LinearRegression | **0.188** | **0.054** | **0.232** |
- **Best Model**: Linear Regression
- 이유: 모든 지표에서 가장 낮은 오차값 기록 → 단순 모델이지만 예측력이 가장 우수

---

### 🔹 성과 및 특징

- **기업 성공 확률을 수치화**하여 투자/전략 의사결정 지원 가능
- 그룹별(국가-산업) 특화 모델 학습으로 일반화 성능 확보
- 회귀 기반 모델 중 **Linear Regression이 가장 우수**하다는 결론 도출

---

## 🚀 프로젝트 요약

---

- **ETL 프로젝트**: 데이터 수집~적재 자동화 파이프라인 구축
- **ML 프로젝트**: 수집된 데이터를 활용하여 실제 예측 모델링 수행

---
