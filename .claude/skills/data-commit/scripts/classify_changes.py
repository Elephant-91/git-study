"""Classify working-tree changes into data-org commit types and group them.

Usage:
    python classify_changes.py [--repo PATH] [--staged-only]

Prints JSON: {"groups": [...], "warnings": [...]}.
Each group = {"type", "scope", "files": [{"path", "status", "reason"}]}.
The classification is a heuristic first pass; the skill refines it by reading diffs.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path, PurePosixPath

LARGE_FILE_BYTES = 10 * 1024 * 1024

# (type, regex on posix path, reason). First match wins, so order = priority.
RULES = [
    ("chore", r"(^|/)\.claude/", "Claude 설정/스킬"),
    ("ci", r"(^|/)\.github/|(^|/)\.gitlab-ci\.yml$|(^|/)\.pre-commit-config\.yaml$|(^|/)Jenkinsfile$", "CI/CD 설정"),
    ("build", r"(^|/)(requirements[^/]*\.txt|pyproject\.toml|setup\.(py|cfg)|environment\.ya?ml|poetry\.lock|uv\.lock|Pipfile(\.lock)?|Dockerfile|docker-compose\.ya?ml|package(-lock)?\.json)$", "의존성/빌드 환경"),
    ("test", r"(^|/)(tests?|great_expectations|expectations)/|(^|/)test_[^/]+\.py$|_test\.py$|(^|/)tests?/.*\.sql$", "테스트/데이터 검증"),
    ("metric", r"(^|/)(metrics|semantic[_-]?layer|semantic_models)/", "지표 정의"),
    ("pipeline", r"(^|/)(dags|airflow|pipelines?|etl|elt|jobs|workflows|prefect|dagster)/|(^|/)dbt_project\.yml$|(^|/)models/.*\.sql$|(^|/)macros/.*\.sql$|(^|/)snapshots/", "ETL/ELT 파이프라인"),
    ("data", r"(^|/)(schema[^/]*\.ya?ml|sources\.ya?ml)$|\.dvc$|(^|/)(seeds|data|datasets|ddl|schemas?)/|\.(csv|tsv|parquet|feather|xlsx?)$", "데이터셋/스키마"),
    ("model", r"(^|/)(ml|models?|training|features?|feature_store|inference)/.*\.py$|(^|/)(train|predict|inference)[^/]*\.py$|(^|/)configs?/.*model[^/]*\.ya?ml$|(^|/)MLproject$", "ML 모델/피처"),
    ("exp", r"(^|/)(experiments?|ab[_-]?tests?)/", "실험"),
    ("analysis", r"\.ipynb$|(^|/)(notebooks?|analysis|analyses|eda|reports?)/|\.(Rmd|qmd)$", "분석/노트북"),
    ("viz", r"(^|/)(dashboards?|viz|visuali[sz]ations?|charts?|plots?)/|\.(twbx?|pbix|lkml)$", "시각화/대시보드"),
    ("docs", r"\.(md|rst|txt)$|(^|/)docs?/", "문서"),
    ("chore", r"(^|/)\.(gitignore|gitattributes|editorconfig|env\.example)$", "설정/잡무"),
]

SECRET_PATH = re.compile(r"(^|/)(\.env(\.[^/]*)?|credentials?[^/]*\.json|service[_-]?account[^/]*\.json|[^/]*\.(pem|key|p12))$", re.I)
SECRET_EXAMPLE = re.compile(r"\.(example|sample|template)$", re.I)
STATUS_NAMES = {"A": "added", "M": "modified", "D": "deleted", "R": "renamed", "C": "copied", "?": "untracked", "T": "typechange", "U": "unmerged"}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def changed_files(repo, staged_only):
    raw = git(repo, "status", "--porcelain=v1", "-z", "-uall").decode("utf-8", "replace")
    entries = raw.split("\0")
    out, i = [], 0
    while i < len(entries):
        e = entries[i]
        i += 1
        if len(e) < 4:
            continue
        x, y, path = e[0], e[1], e[3:]
        if x in "RC":  # rename/copy: next entry is the original path
            i += 1
        if staged_only and x in " ?":
            continue
        code = x if x not in " ?" else y
        out.append({"path": path, "status": STATUS_NAMES.get(code, code), "staged": x not in " ?"})
    return out


def classify(path):
    for typ, pattern, reason in RULES:
        if re.search(pattern, path, re.I):
            return typ, reason
    if path.endswith(".sql"):
        return "pipeline", "SQL"
    return "feat", "기타 소스 (diff 확인 필요: feat/fix/refactor)"


def guess_scope(path, typ):
    p = PurePosixPath(path)
    if typ in ("pipeline", "model", "analysis", "viz", "exp", "metric") and p.suffix:
        return p.stem
    parts = p.parts[:-1]
    if parts:
        return parts[-1] if parts[-1] not in ("src", "lib", ".") else p.stem
    return p.stem.lower()


def notebook_has_outputs(full):
    try:
        nb = json.loads(full.read_text(encoding="utf-8"))
        return any(c.get("outputs") for c in nb.get("cells", []))
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--staged-only", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo)

    try:
        files = changed_files(repo, args.staged_only)
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": e.stderr.decode("utf-8", "replace")}, ensure_ascii=False))
        sys.exit(1)

    groups, warnings = OrderedDict(), []
    for f in files:
        path = f["path"]
        full = repo / path
        if SECRET_PATH.search(path) and not SECRET_EXAMPLE.search(path):
            warnings.append({"path": path, "kind": "secret", "message": "비밀정보 파일로 보임 - 커밋 제외 권장"})
            continue
        if full.is_file():
            if full.stat().st_size > LARGE_FILE_BYTES:
                warnings.append({"path": path, "kind": "large", "message": "10MB 초과 - DVC/외부 스토리지 사용 권장"})
            if path.endswith(".ipynb") and notebook_has_outputs(full):
                warnings.append({"path": path, "kind": "nb-output", "message": "노트북 출력 포함 - nbstripout 후 커밋 권장"})
        typ, reason = classify(path)
        groups.setdefault(typ, []).append({**f, "reason": reason, "scope_hint": guess_scope(path, typ)})

    result = {
        "groups": [{"type": t, "files": fs} for t, fs in groups.items()],
        "warnings": warnings,
    }
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
