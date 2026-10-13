# 데이터 분석 조직용 커밋 메시지 컨벤션 (DA-Commit v1)

[Conventional Commits 1.0.0](https://www.conventionalcommits.org/ko/v1.0.0/)을 기반으로,
데이터 분석 조직에서 자주 발생하는 변경(파이프라인, 노트북, 모델, 데이터 스키마, 대시보드)을
명확히 구분할 수 있도록 **타입을 확장**하고 **데이터 영향도 푸터**를 추가한 규칙입니다.

---

## 1. 형식

```
<type>(<scope>)<!>: <subject>

<body>

<footer>
```

| 요소 | 필수 | 규칙 |
|------|:---:|------|
| `type` | O | 아래 타입 표 중 하나 (영문 소문자) |
| `scope` | △ | 변경 대상 이름 — 파이프라인/DAG명, dbt 모델명, 도메인, 레이어 등. 권장 |
| `!` | X | 하위 호환을 깨는 변경(스키마/지표 정의 변경 등)일 때 콜론 앞에 붙임 |
| `subject` | O | 50자 이내, 한국어 명사형/개조식 종결(`~추가`, `~수정`), 마침표 없음 |
| `body` | △ | **무엇을, 왜** 바꿨는지. 72자 줄바꿈. 분석 결과·수치는 여기에 |
| `footer` | △ | `Token: value` 형식의 git trailer (아래 4절) |

- 콜론 앞에는 공백을 두지 않습니다: `docs: ...` (O) / `docs : ...` (X)
- 하나의 커밋에는 **하나의 논리적 변경**만 담습니다. 타입이 둘 이상 섞이면 커밋을 나눕니다.

---

## 2. 타입

### 2-1. 표준 타입 (Conventional Commits)

| type | 의미 | 데이터 조직에서의 예 |
|------|------|------|
| `feat` | 새로운 기능 | 신규 API, 신규 CLI 옵션, 유틸 함수 추가 |
| `fix` | 버그 수정 | 잘못된 조인 키, 타임존 오류, NULL 처리 누락 수정 |
| `refactor` | 동작 변화 없는 구조 개선 | 공통 전처리 함수 분리, 쿼리 CTE 정리 |
| `perf` | 성능 개선 | 파티션 프루닝, 쿼리 비용 절감, 벡터화 |
| `test` | 테스트 추가/수정 | pytest, dbt test, Great Expectations 검증 |
| `docs` | 문서 | README, 데이터 사전, 지표 정의서 |
| `style` | 포맷팅 (로직 무변화) | black/ruff/sqlfluff 적용 |
| `build` | 의존성/빌드/환경 | requirements.txt, pyproject.toml, Dockerfile |
| `ci` | CI/CD 설정 | GitHub Actions, pre-commit |
| `chore` | 기타 잡무 | .gitignore, 설정 파일 정리 |
| `revert` | 이전 커밋 되돌림 | `revert: feat(mart): ...` |

### 2-2. 데이터 조직 확장 타입

| type | 의미 | 대표 파일 |
|------|------|------|
| `pipeline` | ETL/ELT, 워크플로 변경 | Airflow DAG, dbt 모델(`models/**/*.sql`), Spark job, 스케줄 |
| `data` | 데이터셋·스키마·메타데이터 변경 | `schema.yml`, DDL, seed CSV, DVC 포인터(`*.dvc`), 샘플 데이터 |
| `model` | ML 모델 학습/추론 로직, 피처, 하이퍼파라미터 | `train*.py`, `features/`, `configs/model*.yaml`, MLflow 설정 |
| `analysis` | 탐색적 분석, 애드혹 분석, 리포트 | `*.ipynb`, `notebooks/`, `analysis/`, `reports/` |
| `viz` | 대시보드, 차트, 시각화 | `dashboards/`, `*.twb(x)`, `*.pbix`, Superset/Looker 정의, plot 코드 |
| `exp` | 실험 설정/결과 기록 | A/B 테스트 설계, `experiments/`, 실험 config |
| `metric` | 비즈니스 지표 정의 변경 | 지표 정의 SQL, semantic layer(`metrics/*.yml`) |

> **타입 선택 우선순위** — 한 파일이 여러 타입에 해당하면:
> `fix` > `metric` > `pipeline` > `model` > `data` > `analysis` > `viz` > `exp` > `feat` > `refactor` > 나머지.
> 즉 "버그 수정"이면 위치와 관계없이 `fix(<scope>)`로 쓰고, scope로 영역을 표시합니다.
> 예: dbt 모델의 조인 버그 → `fix(mart_daily_trips): ...`

---

## 3. Scope 가이드

scope는 **나중에 `git log --grep`으로 찾을 이름**을 씁니다.

| 영역 | scope 예 |
|------|----------|
| 파이프라인 | DAG id (`daily_trip_etl`), dbt 모델명 (`stg_rides`, `mart_daily_kpi`) |
| 데이터 레이어 | `raw`, `staging`, `mart`, `feature-store` |
| 도메인 | `mobility`, `user`, `payment`, `vehicle` |
| 모델 | 모델명 (`eta-predictor`, `demand-forecast`) |
| 분석 | 분석 주제 (`churn-eda`, `2026q3-retention`) |
| 대시보드 | 대시보드명 (`ops-dashboard`) |

여러 영역이면 쉼표 없이 상위 개념 하나를 고르거나 생략합니다.

---

## 4. Footer (데이터 영향도 트레일러)

데이터 조직에서는 "코드가 바뀌었다"보다 **"데이터/지표가 어떻게 바뀌는가"**가 더 중요합니다.
해당될 때 아래 트레일러를 붙입니다.

| Token | 언제 | 예 |
|-------|------|----|
| `BREAKING CHANGE:` | 컬럼 삭제/이름 변경, 지표 정의 변경 등 하위 소비자 영향 | `BREAKING CHANGE: trip_fare 컬럼을 fare_krw로 변경` |
| `Data-Impact:` | 재처리·백필 필요, 과거 수치 변동 | `Data-Impact: 2026-09-01 이후 백필 필요` |
| `Schema-Change:` | 테이블 스키마 변경 (비파괴 포함) | `Schema-Change: mart.daily_kpi + active_users(INT)` |
| `Metric:` | 모델/분석 결과 수치 | `Metric: MAPE 12.4% -> 9.8% (valid 2026-09)` |
| `Experiment:` | 실험 추적 ID | `Experiment: mlflow run 3f2a9c` |
| `Refs:` | 이슈/티켓/분석 요청 | `Refs: DA-123` |
| `Co-authored-by:` | 공동 작업자 | `Co-authored-by: Name <email>` |

---

## 5. 데이터 조직 특화 규칙

1. **원본 데이터는 커밋하지 않는다** — 대용량 데이터(대략 10MB 이상), `*.parquet`, `*.csv` 원본은 DVC/스토리지에 두고 포인터만 커밋 (`data` 타입).
2. **노트북은 출력 제거 후 커밋** — 출력이 포함된 `.ipynb`는 diff를 가린다. `nbstripout` 등으로 정리하고, 결과 수치는 body/`Metric:` 트레일러에 기록.
3. **비밀정보 금지** — `.env`, credential JSON, 접속 문자열이 있는 파일은 커밋 대상에서 제외.
4. **지표 정의 변경은 반드시 `!` 또는 `BREAKING CHANGE`** — 대시보드 소비자가 수치 변화를 추적할 수 있게.
5. **스키마 변경은 코드와 같은 커밋에** — DDL/`schema.yml` 변경과 이를 사용하는 모델 SQL은 같은 커밋으로 묶는다(원자성).

---

## 6. 예시

```
pipeline(daily_trip_etl): 일별 운행 집계 DAG에 재시도 정책 추가

외부 API 타임아웃으로 새벽 배치가 간헐적으로 실패하여
retries=3, retry_delay=10m 설정을 추가함.

Refs: DA-412
```

```
fix(stg_rides)!: 운행 시작 시각 타임존을 KST로 변환

UTC 그대로 적재되어 일 단위 집계가 9시간 밀려 있었음.

BREAKING CHANGE: started_at 컬럼이 KST 기준으로 변경됨
Data-Impact: 2026-01-01 이후 mart_daily_kpi 백필 필요
```

```
model(demand-forecast): 기상 피처 추가 및 학습 기간 확대

Metric: MAPE 12.4% -> 9.8% (valid 2026-09)
Experiment: mlflow run 3f2a9c
```

```
analysis(churn-eda): 3분기 이탈 사용자 코호트 분석 노트북 추가
```

```
docs(readme): Git 기본 사용법 정리 문서 보완
```

---

## 참고 자료

- Conventional Commits 1.0.0 — https://www.conventionalcommits.org/ko/v1.0.0/
- Angular Commit Message Guidelines — https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit
- Git trailers — https://git-scm.com/docs/git-interpret-trailers
- Git workflows for data teams — https://dataexpert.io/blog/git-workflows-for-data-teams
