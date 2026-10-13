---
name: gh-issue
description: 새 기능 추가·버그 수정·문서 작업 등을 시작할 때 사용자 요청을 바탕으로 GitHub 이슈 제목·본문을 작성하고, 유형(type)·우선순위(priority) 라벨을 달아 gh CLI로 이슈를 생성한 뒤 이슈 번호가 들어간 작업 브랜치를 만들어 이동한다. 사용자가 "이슈 만들어줘", "이슈 등록", "이슈 생성", "새 기능 추가할 거야", "버그 이슈", "/gh-issue" 등을 요청할 때 사용한다.
---

# gh-issue

**사전 점검 → 라벨 준비 → 이슈 작성 → 생성 → 브랜치 생성 → 결과 보고** 순서로 처리한다.
라벨 정의와 유형 판별 기준은 [references/labels.md](references/labels.md),
본문 템플릿은 [references/issue-template.md](references/issue-template.md)에 있으며, 작성 전에 읽는다.

## 1. 사전 점검

```bash
gh auth status
git remote get-url origin
git status --short
```

- `gh`가 로그인되어 있지 않으면 사용자에게 터미널에서 `gh auth login`을 실행하라고 안내하고 종료한다. (토큰을 대신 입력하지 않는다)
- `origin`이 없으면 이슈를 만들 저장소를 사용자에게 묻는다.
- `git status` 결과는 5단계 브랜치 생성 시 안내용으로 기억해 둔다.

## 2. 라벨 준비

```bash
python .claude/skills/gh-issue/scripts/ensure_labels.py
```

- 저장소에 없는 `type: *`, `priority: *` 라벨만 생성한다(여러 번 실행해도 안전).
- 출력 JSON의 `created`가 비어 있지 않으면 결과 보고 때 "라벨 N개를 새로 만들었다"고 함께 알린다.
- `error`가 있으면 내용을 보고하고 중단한다.

## 3. 이슈 내용 작성

사용자 발화에서 다음을 정한다.

| 항목 | 규칙 |
|------|------|
| 유형 | labels.md의 키워드 기준으로 `feature`/`bug`/`docs`/`refactor`/`chore` 중 하나 |
| 우선순위 | 언급이 있으면 그대로("급해", "긴급" → high, "나중에", "여유" → low), 없으면 `medium` |
| 제목 | `[Feature] 로그인 폼 검증 추가` 형식. 대괄호 태그는 유형별 고정(labels.md), 한국어, 50자 이내, 마침표 없음 |
| 본문 | issue-template.md의 유형별 템플릿을 채운다 |

- 요청이 너무 모호해 **제목조차 정할 수 없을 때만** 한 번 질문한다. 그 외에는 바로 진행한다.
- 본문에는 사용자 발화·저장소 내용에 근거가 있는 것만 쓴다. 모르는 항목은 `- [ ] (작성 필요)`처럼 비워 두고 지어내지 않는다.
- 사용자가 한 번에 여러 작업을 말하면 작업마다 이슈를 따로 만든다.

## 4. 이슈 생성

본문은 스크래치패드(없으면 임시 디렉터리)에 **UTF-8** 파일로 저장해 전달한다 (한글 깨짐 방지).

```bash
gh issue create \
  --title "[Feature] 로그인 폼 검증 추가" \
  --body-file <body.md> \
  --label "type: feature" \
  --label "priority: medium"
```

- 출력되는 이슈 URL(`.../issues/<번호>`)에서 번호를 추출한다.
- 사용자가 담당자·마일스톤을 말했다면 `--assignee`, `--milestone`을 추가한다.

## 5. 작업 브랜치 생성

```bash
git switch -c <prefix>/<번호>-<slug>
```

- prefix: feature → `feature`, bug → `fix`, docs → `docs`, refactor → `refactor`, chore → `chore`
- slug: 제목을 영어 소문자 kebab-case로 2~5단어 (예: `feature/12-login-form-validation`)
- 같은 이름의 브랜치가 이미 있으면 새로 만들지 않고 사용자에게 알린다.
- 1단계에서 커밋되지 않은 변경이 있었다면 "현재 변경 사항이 새 브랜치로 함께 옮겨졌다"고 알린다.
- 사용자가 브랜치는 필요 없다고 하면 이 단계를 건너뛴다.
- push는 사용자가 요청할 때만 한다 (`git push -u origin <브랜치>`).

## 6. 결과 보고

```
✅ 이슈 #12 생성: https://github.com/<owner>/<repo>/issues/12
   제목  : [Feature] 로그인 폼 검증 추가
   라벨  : type: feature, priority: medium
   브랜치: feature/12-login-form-validation (이동 완료)
```

이어서 다음을 안내한다.

- 커밋할 때 footer에 `Refs: #12` (data-commit 스킬 사용 시 자동 반영되도록 이슈 번호를 알려 준다)
- PR 본문에 `Closes #12`를 쓰면 병합 시 이슈가 자동으로 닫힌다.
