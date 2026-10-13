"""저장소에 gh-issue 스킬용 type/priority 라벨이 없으면 생성한다.

사용법:
    python ensure_labels.py [--repo OWNER/REPO] [--dry-run]

출력(JSON): {"created": [...], "existing": [...], "error": null}
"""
import argparse
import json
import subprocess
import sys

# references/labels.md와 동일하게 유지한다.
LABELS = [
    ("type: feature", "a2eeef", "새로운 기능 추가"),
    ("type: bug", "d73a4a", "잘못 동작하는 부분 수정"),
    ("type: docs", "0075ca", "문서 작성 및 보완"),
    ("type: refactor", "cfd3d7", "동작 변화 없는 코드 구조 개선"),
    ("type: chore", "fef2c0", "설정, 의존성, 빌드 등 기타 작업"),
    ("priority: high", "b60205", "우선순위 높음 - 즉시 처리"),
    ("priority: medium", "fbca04", "우선순위 보통"),
    ("priority: low", "0e8a16", "우선순위 낮음 - 여유 있을 때"),
]


def run_gh(args, repo):
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="OWNER/REPO (생략 시 현재 디렉터리의 origin)")
    parser.add_argument("--dry-run", action="store_true", help="생성하지 않고 생성 예정 목록만 출력")
    opts = parser.parse_args()

    result = {"created": [], "existing": [], "error": None}

    listed = run_gh(["label", "list", "--json", "name", "--limit", "500"], opts.repo)
    if listed.returncode != 0:
        result["error"] = f"라벨 목록 조회 실패: {listed.stderr.strip()}"
        if not opts.dry_run:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1
        existing = set()
    else:
        existing = {label["name"].lower() for label in json.loads(listed.stdout or "[]")}

    for name, color, description in LABELS:
        if name.lower() in existing:
            result["existing"].append(name)
            continue
        if not opts.dry_run:
            made = run_gh(
                ["label", "create", name, "--color", color, "--description", description],
                opts.repo,
            )
            if made.returncode != 0:
                result["error"] = f"'{name}' 생성 실패: {made.stderr.strip()}"
                break
        result["created"].append(name)

    if opts.dry_run:
        result["dry_run"] = True
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["error"] and not opts.dry_run else 0


if __name__ == "__main__":
    sys.exit(main())
