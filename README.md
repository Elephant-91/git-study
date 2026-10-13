# Day 3 — Claude Code로 만드는 세컨드 브레인

Tiago Forte의 **BASB(Building a Second Brain)** 방법론을 바탕으로, Claude Code 스킬을 이용해 지식을 **수집(`/ingest`)** 하고 **검색(`/query`)** 하는 개인 지식 관리(PKM) 볼트를 만든 실습 기록이다.

> 뇌는 아이디어를 저장하는 곳이 아니라 만들어내는 곳이다.
> 저장과 정리는 시스템과 AI에 맡기고, 사람은 생각과 연결에 집중한다.

> **참고**: 현재 저장소에는 `main` 브랜치만 남아 있다. 2~4번 작업(`/query` 스킬, 수집 노트)은 `add-data-org-wiki-note` 브랜치에 있던 커밋(`c1e0a91`)이었으나 브랜치를 삭제해 `main`에 포함되지 않았다. 필요하면 `git branch <이름> c1e0a91`로 복구할 수 있다.

---

## 진행한 내용

| 순서 | 작업 | 결과물 | 위치 |
|------|------|--------|------|
| 1 | 세컨드 브레인 방법론 조사·정리 (BASB의 CODE·PARA, 제텔카스텐, 도구 비교, 운영 원칙, 실천 루틴) | [second-brain-guide.md](second-brain-guide.md) | `main` |
| 2 | 입력(URL·파일·텍스트)을 PARA 규칙에 맞춘 노트로 저장하는 `/ingest` 스킬 제작 | [.claude/skills/ingest/SKILL.md](.claude/skills/ingest/SKILL.md) | `main` |
| 3 | `/ingest`로 첫 노트 수집: 데이터 분석 조직용 위키 구조 레퍼런스 | `3_Resources/지식관리/2026-10-13-데이터조직-위키구조-레퍼런스.md`, `_ingest-log.md` | 삭제된 브랜치 (`c1e0a91`) |
| 4 | 쌓인 노트를 키워드·질문·메타데이터로 찾는 읽기 전용 `/query` 스킬 제작 | `.claude/skills/query/SKILL.md` | 삭제된 브랜치 (`c1e0a91`) |

---

## 폴더 구조

```
day3/
├── README.md
├── second-brain-guide.md          # 세컨드 브레인 구축 가이드 (방법론 정리)
├── _ingest-log.md                 # /ingest 수집 기록 (최신이 위)
├── 0_Inbox/                       # 분류가 애매한 노트
├── 1_Projects/                    # 기한·목표가 있는 일
├── 2_Areas/                       # 꾸준히 책임지는 분야
├── 3_Resources/                   # 관심 주제 참고 자료
│   └── 지식관리/
│       └── 2026-10-13-데이터조직-위키구조-레퍼런스.md
├── 4_Archives/                    # 완료·비활성 항목
└── .claude/skills/
    ├── ingest/SKILL.md            # /ingest 스킬
    └── query/SKILL.md             # /query 스킬
```

PARA 폴더는 `/ingest`가 노트를 저장할 때 필요한 것만 자동으로 만든다. (Git은 빈 폴더를 추적하지 않으므로 `0_Inbox`, `1_Projects`, `2_Areas`, `4_Archives`는 디스크에만 존재한다.)

---

## 핵심 개념 요약

자세한 내용은 [second-brain-guide.md](second-brain-guide.md)에 있다.

- **CODE**: Capture(와닿는 것만 수집) → Organize(주제가 아니라 쓰임새 기준으로 분류) → Distill(점진적 요약) → Express(결과물로 만들기)
- **PARA**: 실행 가능성 순으로 Projects → Areas → Resources → Archives에 분류한다. 끝난 프로젝트는 지우지 않고 Archives로 옮긴다.
- **점진적 요약**: 핵심은 **굵게**, 그중 가장 중요한 부분은 ==형광펜==, 맨 위에 한 줄 요약을 단다.
- **제텔카스텐**: 노트 하나에 아이디어 하나, 자기 말로 쓰기, `[[링크]]`로 연결하기.
- **AI 활용 원칙**: 분류·태깅·요약 같은 지루한 일은 AI에 맡기고, 생각과 연결은 사람이 검토한다. 데이터는 로컬 Markdown으로 직접 소유한다.

---

## 스킬 사용법

### `/ingest` — 지식 수집

```
/ingest https://example.com/article        # URL
/ingest ./docs/회의록.pdf                   # 파일 (PDF, DOCX, HWP 등)
/ingest 오늘 배운 내용을 길게 적은 텍스트…    # 직접 입력
```

동작 순서:

1. **입력 유형 판별**: URL이면 WebFetch로 가져오고, 파일이면 읽고, 그 밖의 입력은 텍스트로 처리한다.
2. **PARA 분류**: Projects → Areas → Resources → Archives 순으로 처음 맞는 곳에 넣는다. 판단 근거가 부족하면 `0_Inbox`에 넣는다. 새 프로젝트 폴더는 만들지 않고 제안만 한다.
3. **요약**: 한 줄 요약, 핵심 내용 3~7개(굵게·형광펜 표시), 활용 아이디어 1~3개를 쓴다.
4. **관련 노트 연결**: 키워드로 볼트를 검색해 실제로 관련 있는 노트만 최대 5개 `[[링크]]`로 연결한다. 같은 출처의 노트가 이미 있으면 새로 만들지 않고 갱신할지 묻는다.
5. **저장**: `YYYY-MM-DD-<slug>.md` 파일명과 고정 템플릿으로 저장한다.
6. **기록**: `_ingest-log.md` 표 맨 위에 한 줄을 추가한다.

노트 frontmatter:

```yaml
title / created / type(url|file|text) / source / author / published
para / category / para_reason / tags / status(seed → distilled → expressed)
```

### `/query` — 볼트 검색 (읽기 전용)

```
/query                                      # 개요: PARA별 노트 수, 최근 수집, 상위 태그, Inbox 현황
/query ADR                                  # 검색: 관련 노트를 순위대로 최대 7개
/query 지표 정의 변경은 어떻게 기록해?        # 답변: 노트 내용만 근거로 출처를 달아 답변
/query 위키 para:R tag:ADR status:seed      # 메타데이터 필터 조합
```

| 필터 | 예시 |
|------|------|
| `para:` | `para:R` (P/A/R/Ar/I 약어 허용) |
| `cat:` | `cat:지식관리` |
| `tag:` | `tag:Diataxis` |
| `status:` | `status:seed` |
| `type:` | `type:url` |
| `after:` / `before:` | `after:2026-10-01` |

- 한·영 대응어와 띄어쓰기 변형으로 검색어를 넓힌다 (예: `의사결정 기록` ↔ `ADR`).
- 제목·태그·한 줄 요약·형광펜에서 맞은 노트에 가중치를 준다.
- 답변 모드에서는 노트에 없는 내용을 일반 지식으로 채우지 않고, 보충할 때는 따로 구분해서 표시한다.
- 읽기 전용이라 노트를 만들거나 고치지 않는다.

---

## 수집한 노트

| 날짜 | 제목 | PARA | 태그 |
|------|------|------|------|
| 2026-10-13 | [데이터 분석 조직용 위키 구조 레퍼런스](3_Resources/지식관리/2026-10-13-데이터조직-위키구조-레퍼런스.md) | Resources/지식관리 | 사내위키, 데이터조직, 문서화, ADR, Diataxis |

> 데이터 분석 조직의 위키는 Diátaxis로 문서 유형을 나누고 ADR로 지표 정의의 결정 이력을 남기는 것이 핵심이다. KCS와 Handbook-first로 운영하고, LLM Wiki 패턴으로 지표 정의 충돌을 자동 점검할 수 있다.

---

## 운영 루틴

| 주기 | 할 일 |
|------|-------|
| 매일 (5분) | 와닿은 내용을 `/ingest`로 수집한다. 분류가 애매하면 Inbox에 둔다. |
| 매주 (30분) | `/query`로 현황을 보고 Inbox를 비운다. 다시 본 노트는 `status`를 `distilled`로 올리고, 끝난 프로젝트는 Archives로 옮긴다. |
| 매월 | 노트로 결과물을 하나 만들고(Express) `status`를 `expressed`로 바꾼다. |

---

## 다음에 해볼 것

- [ ] 진행 중인 프로젝트 폴더를 `1_Projects/`에 만들어 프로젝트 우선 분류 시험하기
- [ ] 노트를 여러 개 수집해 `/query`의 순위와 관련 노트 연결 품질 확인하기
- [ ] Obsidian으로 볼트를 열어 그래프 뷰로 `[[링크]]` 연결 확인하기
- [ ] 점진적 요약 단계를 올리는 스킬(예: `/distill`) 검토하기
