---
name: data-commit
description: 데이터 분석 조직용 커밋 컨벤션(Conventional Commits 확장, DA-Commit v1)에 따라 작업 트리의 변경 사항을 분석해 비슷한 유형의 파일끼리 묶고, 그룹별 커밋 메시지를 작성해 나눠서 커밋한다. 사용자가 "커밋 메시지 작성", "변경사항 커밋", "커밋 나눠줘", "commit", "/data-commit" 등을 요청할 때, 특히 dbt·Airflow·노트북·ML 모델·대시보드·스키마 변경이 섞인 저장소에서 사용한다.
---

# data-commit

변경 파일을 **분류 → 그룹핑 → 메시지 작성 → 확인 → 커밋** 순서로 처리한다.
컨벤션 전문은 [references/convention.md](references/convention.md)에 있으며, 메시지를 쓰기 전에 반드시 읽는다.

## 1. 변경 사항 수집

```bash
python .claude/skills/data-commit/scripts/classify_changes.py --repo .
```

- 이미 스테이징한 것만 다루라는 요청이면 `--staged-only`를 붙인다.
- 출력 JSON의 `groups`는 경로 기반 1차 분류, `warnings`는 커밋 전 경고다.
- 변경이 없으면 "커밋할 변경 사항이 없습니다"라고 알리고 종료한다.

## 2. 경고 처리 (커밋 전에 먼저)

| kind | 처리 |
|------|------|
| `secret` | 이미 그룹에서 제외됨. 사용자에게 알리고 `.gitignore` 추가를 제안. 사용자가 명시적으로 원하지 않는 한 커밋하지 않는다 |
| `large` | DVC/외부 스토리지 사용을 권장하고, 포함 여부를 사용자에게 묻는다 |
| `nb-output` | 출력 제거(`nbstripout` 또는 `jupyter nbconvert --clear-output --inplace`)를 제안. 결과 수치가 필요하면 body/`Metric:`에 옮긴다 |

## 3. diff를 읽고 그룹 다듬기

경로 기반 분류는 출발점일 뿐이다. 각 파일의 diff를 확인해 조정한다.

```bash
git diff -- <path>          # unstaged
git diff --cached -- <path> # staged
```

신규(untracked) 파일은 내용을 직접 읽는다. 조정 기준:

1. **의도 우선** — 버그 수정이면 위치와 상관없이 `fix(<scope>)`. 동작 변화 없는 정리는 `refactor`, 포맷만 바뀌면 `style`.
   `feat` 그룹(기타 소스)은 diff를 보고 `feat`/`fix`/`refactor`/`perf` 중 하나로 확정한다.
2. **원자성** — 스키마 변경(`schema.yml`, DDL)과 이를 사용하는 모델 SQL, 그 테스트는 하나의 커밋으로 합친다.
   코드와 그 코드의 단위 테스트도 같은 커밋이 자연스러우면 합친다.
3. **분리** — 같은 타입이라도 서로 무관한 대상(다른 DAG, 다른 분석 주제)이면 scope별로 나눈다.
4. **크기** — 한 커밋에 대략 10개 이상 파일이 무관하게 섞이면 더 쪼갤 수 있는지 검토한다.
5. **파괴적 변경 탐지** — diff에서 컬럼 삭제/이름 변경, 지표 계산식 변경, 테이블 rename이 보이면 `!`와 `BREAKING CHANGE:`를 붙이고, 재처리가 필요하면 `Data-Impact:`를 쓴다.
6. 그룹 커밋 순서: `build`/`ci`/`chore` → `data` → `pipeline`/`metric` → `model` → `feat`/`fix`/`refactor`/`perf` → `test` → `analysis`/`exp`/`viz` → `docs`. (의존되는 쪽을 먼저)

## 4. 메시지 작성

형식: `<type>(<scope>)<!>: <subject>` + 빈 줄 + body + 빈 줄 + footer

- subject: 한국어, 50자 이내, `~추가`/`~수정`/`~변경` 등 개조식 종결, 마침표 없음, 콜론 앞 공백 없음.
- scope: `scope_hint`를 참고하되, 나중에 검색할 이름(DAG id, dbt 모델명, 모델명, 분석 주제)으로 정한다.
- body: 변경이 자명하지 않을 때만. **왜** 바꿨는지 위주, 72자 줄바꿈.
- footer: 해당될 때만 `Refs:`, `Data-Impact:`, `Schema-Change:`, `Metric:`, `Experiment:`, `BREAKING CHANGE:`.
  티켓 번호·실험 ID·성능 수치는 diff나 사용자 발화에 근거가 있을 때만 쓰고, 지어내지 않는다.
- 저장소에 별도의 커밋 attribution 규칙(시스템/CLAUDE.md)이 있으면 마지막 footer로 따른다.

## 5. 사용자 확인

커밋하기 전에 계획을 표로 보여주고 승인받는다.

```
| # | 커밋 메시지 (subject) | 파일 |
|---|------|------|
| 1 | build: pandas 2.2 버전 고정 | requirements.txt |
| 2 | pipeline(daily_trip_etl): 재시도 정책 추가 | dags/daily_trip_etl.py |
| 3 | docs(readme): 실행 방법 보완 | README.md |
```

경고 항목과 body/footer가 있는 메시지는 표 아래에 전문을 함께 보여준다.
사용자가 "메시지만 작성해줘"라고 했다면 여기서 멈추고 메시지만 제공한다.

## 6. 커밋 실행

승인 후 그룹 순서대로 실행한다. 다른 그룹 파일이 섞이지 않도록 매번 스테이징을 초기화한다.

```bash
git reset -q                       # 스테이징 비우기 (작업 트리 변경은 유지)
git add -- <file1> <file2> ...     # 삭제된 파일도 git add로 스테이징됨
git commit -F <message-file>       # 여러 줄 메시지는 임시 파일로 전달
```

- 메시지 파일은 스크래치패드/임시 디렉터리에 UTF-8로 작성한다 (한글 깨짐 방지).
- `--staged-only` 모드였다면 `git reset`을 하지 말고, 그룹별로 `git restore --staged`/`git add`로 조정한다.
- 훅 실패 시 `--no-verify`로 우회하지 말고 원인을 보고한다.
- push는 사용자가 요청할 때만 한다.

마지막에 `git log --oneline -n <커밋 수>`로 결과를 보여준다.
