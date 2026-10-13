# git-study

Git 기본 사용법을 정리한 학습용 저장소입니다.

---

## 1. Git이란?

Git은 파일의 **변경 이력을 기록하고 관리하는 버전 관리 시스템(VCS)** 입니다.

- 언제, 누가, 무엇을, 왜 바꿨는지 기록할 수 있습니다.
- 이전 시점의 상태로 언제든 되돌아갈 수 있습니다.
- 여러 사람이 같은 프로젝트에서 동시에 작업해도 충돌을 관리할 수 있습니다.

---

## 2. 핵심 개념

| 용어 | 설명 |
|------|------|
| **Repository (저장소)** | 프로젝트 파일과 변경 이력(`.git` 폴더)을 담고 있는 공간 |
| **Working Directory (작업 디렉터리)** | 실제로 파일을 편집하는 작업 공간 |
| **Staging Area (스테이징 영역)** | 다음 커밋에 포함할 변경 사항을 골라 담아두는 곳 |
| **Commit (커밋)** | 스테이징된 변경을 하나의 기록으로 저장한 것 |
| **Branch (브랜치)** | 독립적으로 작업하기 위한 커밋 흐름 |
| **HEAD** | 현재 작업 중인 브랜치 또는 커밋을 가리키는 포인터 |
| **Remote (원격 저장소)** | GitHub 등 인터넷에 있는 저장소 (기본 이름: `origin`) |

### 파일의 상태 흐름

```
Untracked / Modified  ──git add──▶  Staged  ──git commit──▶  Committed
        ▲                                                       │
        └────────────────── 파일 수정 ◀─────────────────────────┘
```

---

## 3. 처음 설정하기

Git을 처음 설치한 뒤 한 번만 사용자 정보를 등록합니다.

```bash
git config --global user.name "본인이름"
git config --global user.email "본인이메일@example.com"
```

설정 확인:

```bash
git config --list
```

기본 브랜치 이름을 `main`으로 설정하려면:

```bash
git config --global init.defaultBranch main
```

---

## 4. 저장소 만들기 / 가져오기

### 새 저장소 만들기

```bash
mkdir my-project
cd my-project
git init
```

### 기존 원격 저장소 복제하기

```bash
git clone https://github.com/사용자명/저장소명.git
```

---

## 5. 기본 작업 흐름 (가장 많이 쓰는 명령어)

### 상태 확인

```bash
git status          # 변경된 파일, 스테이징 상태 확인
```

### 변경 내용 확인

```bash
git diff            # 작업 디렉터리 변경 내용 (스테이징 전)
git diff --staged   # 스테이징된 변경 내용 (커밋 전 최종 확인)
```

### 스테이징

```bash
git add 파일명          # 특정 파일만 추가
git add .               # 현재 위치의 모든 변경 추가
git add -p              # 변경 조각(hunk) 단위로 골라서 추가
```

### 커밋

```bash
git commit -m "커밋 메시지"
```

좋은 커밋 메시지 예시:

```
Add login form validation
Fix typo in README
Remove unused import in main.py
```

- 첫 줄은 50자 안팎으로 간결하게 작성합니다.
- **무엇을** 바꿨는지, 필요하면 **왜** 바꿨는지를 적습니다.

### 커밋 이력 보기

```bash
git log                       # 전체 이력
git log --oneline             # 한 줄씩 간략하게
git log --oneline --graph     # 브랜치 그래프와 함께
git log -p                    # 각 커밋의 변경 내용까지
```

---

## 6. 되돌리기

| 상황 | 명령어 |
|------|--------|
| 수정한 내용을 버리고 마지막 커밋 상태로 되돌리기 | `git restore 파일명` |
| 스테이징을 취소하기 (파일 내용은 유지) | `git restore --staged 파일명` |
| 마지막 커밋 메시지만 수정하기 | `git commit --amend -m "새 메시지"` |
| 마지막 커밋 취소하기 (변경 내용은 유지) | `git reset --soft HEAD~1` |
| 특정 커밋의 변경을 되돌리는 새 커밋 만들기 (안전) | `git revert 커밋해시` |

> ⚠️ `git reset --hard`는 작업 중인 변경 내용을 **영구적으로 삭제**합니다. 실행 전에 한 번 더 확인하세요.
>
> ⚠️ 이미 원격(push)에 올린 커밋은 `--amend`나 `reset`으로 고치지 않는 것이 좋습니다. 대신 `git revert`를 사용합니다.

---

## 7. 브랜치

브랜치는 `main`을 해치지 않고 새 기능이나 실험을 진행하기 위해 사용합니다.

```bash
git branch                  # 브랜치 목록 확인
git branch 새브랜치이름       # 브랜치 생성
git switch 새브랜치이름       # 브랜치 이동 (최신 방식)
git switch -c 새브랜치이름    # 생성과 이동을 한 번에
git branch -d 브랜치이름      # 병합이 끝난 브랜치 삭제
```

> `git checkout`으로도 브랜치를 옮길 수 있지만, 최근에는 `git switch`와 `git restore`로 역할이 나뉘어 있어 더 명확합니다.

### 브랜치 병합 (merge)

```bash
git switch main
git merge 작업브랜치이름
```

### 충돌(conflict) 해결

같은 파일의 같은 부분을 서로 다르게 수정하면 병합 시 충돌이 발생합니다.

```
<<<<<<< HEAD
현재 브랜치의 내용
=======
합치려는 브랜치의 내용
>>>>>>> 작업브랜치이름
```

1. 충돌 표시 부분을 열어 원하는 최종 내용만 남기고 `<<<<<<<`, `=======`, `>>>>>>>` 표시를 지웁니다.
2. 파일을 저장한 뒤 스테이징하고 커밋합니다.

```bash
git add 파일명
git commit
```

---

## 8. 원격 저장소 (GitHub)

```bash
git remote -v                       # 원격 저장소 주소 확인
git remote add origin 주소          # 원격 저장소 연결
git push -u origin main             # 처음 올릴 때 (-u: 기본 연결 설정)
git push                            # 이후 올리기
git pull                            # 원격 변경 내용 가져와 병합
git fetch                           # 원격 변경 내용만 가져오기 (병합은 안 함)
```

### 작업 흐름 예시

```bash
git switch -c feature/login         # 1. 기능 브랜치 생성
# ... 파일 수정 ...
git add .                           # 2. 스테이징
git commit -m "Add login form"      # 3. 커밋
git push -u origin feature/login    # 4. 원격에 브랜치 올리기
# 5. GitHub에서 Pull Request 생성 → 리뷰 → main에 병합
git switch main
git pull                            # 6. 병합된 최신 main 받기
```

---

## 9. `.gitignore`

Git이 추적하지 않았으면 하는 파일(비밀번호, 빌드 결과물, 가상환경 등)은 `.gitignore`에 적습니다.

```gitignore
# 비밀 정보
.env

# 의존성 / 빌드 결과물
node_modules/
dist/
__pycache__/

# 운영체제 / 에디터 설정
.DS_Store
.vscode/
```

> 이미 추적 중인 파일은 `.gitignore`에 추가해도 계속 추적됩니다. `git rm --cached 파일명`으로 추적을 해제한 뒤 커밋하세요.

---

## 10. 자주 쓰는 명령어 요약

```bash
git init                    # 저장소 생성
git clone 주소              # 저장소 복제
git status                  # 상태 확인
git add .                   # 전체 스테이징
git commit -m "메시지"      # 커밋
git log --oneline           # 이력 확인
git switch -c 브랜치        # 브랜치 생성 후 이동
git merge 브랜치            # 브랜치 병합
git pull                    # 원격 최신 내용 받기
git push                    # 원격에 올리기
git restore 파일            # 변경 취소
```

---

## 참고 자료

- [Pro Git 책 (한국어판)](https://git-scm.com/book/ko/v2)
- [Git 공식 문서](https://git-scm.com/docs)
- [GitHub Docs](https://docs.github.com)
