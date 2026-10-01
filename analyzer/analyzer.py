#!/usr/bin/env python3
"""Analyzer: select only the tests affected by a change in a microservice repo.

Language-agnostic: works from git diffs, file layout and build markers
(pom.xml, package.json, *.csproj, go.mod, ...), not from parsing source code.
Writes analyzer_result.json for GitHub Actions / Jenkins to consume.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
SKIP_DIRS = {".git", "node_modules", "target", "bin", "obj", "dist", "build",
             "__pycache__", ".venv", "venv", ".idea", ".vscode", "analyzer"}

# build marker -> (language, test command)
MARKERS = {
    "pom.xml": ("java", "mvn test"),
    "build.gradle": ("java", "gradle test"),
    "build.gradle.kts": ("kotlin", "gradle test"),
    "package.json": ("javascript", "npm test"),
    "go.mod": ("go", "go test ./..."),
    "requirements.txt": ("python", "pytest"),
    "pyproject.toml": ("python", "pytest"),
    "Cargo.toml": ("rust", "cargo test"),
    "Gemfile": ("ruby", "bundle exec rspec"),
    "composer.json": ("php", "vendor/bin/phpunit"),
}
EXT_LANG = {".java": "java", ".kt": "kotlin", ".js": "javascript", ".ts": "typescript",
            ".cs": "csharp", ".go": "go", ".py": "python", ".rs": "rust", ".rb": "ruby",
            ".php": "php", ".scala": "scala", ".swift": "swift", ".cpp": "cpp", ".c": "c"}
CONFIG_NAMES = {"Dockerfile", "docker-compose.yml", "Makefile", "Jenkinsfile", ".env"} | set(MARKERS)
CONFIG_EXT = {".yml", ".yaml", ".json", ".toml", ".ini", ".env", ".properties", ".xml",
              ".conf", ".cfg", ".csproj", ".sln", ".gradle", ".tf"}
DOC_EXT = {".md", ".rst", ".txt"}
IGNORE_NAMES = {".gitignore", ".gitattributes", "analyzer_result.json"}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs"}
TEST_NAME = re.compile(r"(Tests?\.\w+$|Tests?Case\.\w+$|IT\.\w+$|\.(test|spec)\.\w+$|_test\.\w+$|^test_.*\.py$)")


def run(cmd, cwd, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode and check:
        sys.exit(f"git error: {r.stderr.strip()}")
    return r.stdout if r.returncode == 0 else None


def is_test(rel):
    p = Path(rel)
    return any(x.lower() in TEST_DIRS for x in p.parts[:-1]) or bool(TEST_NAME.search(p.name))


def is_integration(rel):
    low = rel.lower()
    return "integration" in low or "e2e" in low or bool(re.search(r"IT\.\w+$", rel))


def classify(rel):
    p = Path(rel)
    if p.name in IGNORE_NAMES:
        return "ignored"
    if is_test(rel):
        return "test"
    if p.suffix in DOC_EXT:
        return "docs"
    if p.name in CONFIG_NAMES or p.suffix in CONFIG_EXT:
        return "config"
    if p.suffix in EXT_LANG:
        return "source"
    return "other"


def norm(stem):
    s = re.sub(r"(tests?|spec|it)$", "", stem.lower())
    return re.sub(r"[^a-z0-9]", "", s)


# ---------- service discovery ----------
def has_marker(d):
    for f in d.iterdir():
        if f.is_file() and (f.name in MARKERS or f.name == "Dockerfile" or f.suffix in (".csproj", ".sln")):
            return True
    return False


def describe_service(d, root):
    lang, cmd = None, None
    for f in sorted(d.iterdir()):
        if f.is_file() and f.name in MARKERS:
            lang, cmd = MARKERS[f.name]
            break
        if f.is_file() and f.suffix == ".csproj":
            lang, cmd = "csharp", "dotnet test"
            break
    if not lang:  # fall back to the most common source extension
        counts = {}
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in EXT_LANG and not (set(f.parts) & SKIP_DIRS):
                counts[EXT_LANG[f.suffix]] = counts.get(EXT_LANG[f.suffix], 0) + 1
        lang = max(counts, key=counts.get) if counts else "unknown"
    rel = d.relative_to(root).as_posix() or "."
    return {"name": d.name if rel != "." else root.name, "path": rel, "language": lang, "test_command": cmd}


def find_services(root, exclude):
    found = []

    def walk(d):
        for e in sorted(os.scandir(d), key=lambda x: x.name):
            if not e.is_dir() or e.name in SKIP_DIRS or e.name in exclude:
                continue
            p = Path(e.path)
            if has_marker(p):
                found.append(describe_service(p, root))
            else:
                walk(p)
    walk(root)
    return found or [describe_service(root, root)]


def service_of(rel, services):
    for s in sorted(services, key=lambda s: -len(s["path"])):
        if s["path"] == "." or rel == s["path"] or rel.startswith(s["path"] + "/"):
            return s
    return None


# ---------- git ----------
def default_base(repo):
    if os.environ.get("GITHUB_BASE_REF"):
        return "origin/" + os.environ["GITHUB_BASE_REF"]
    if os.environ.get("GIT_PREVIOUS_SUCCESSFUL_COMMIT"):
        return os.environ["GIT_PREVIOUS_SUCCESSFUL_COMMIT"]
    return "HEAD~1" if run(["git", "rev-parse", "--verify", "HEAD~1"], repo, check=False) else EMPTY_TREE


def changed_files(repo, base, head, working):
    if working:
        out = run(["git", "diff", "--name-status", "-M", base], repo)
        out += "".join(f"A\t{f}\n" for f in run(["git", "ls-files", "--others", "--exclude-standard"], repo).split("\n") if f)
    else:
        spec = f"{base}..{head}" if base == EMPTY_TREE else f"{base}...{head}"
        out = run(["git", "diff", "--name-status", "-M", spec], repo)
    changes = []
    for line in out.splitlines():
        parts = line.split("\t")
        status = parts[0][0]
        for path in parts[1:]:
            changes.append({"path": path, "status": status})
    return changes


# ---------- analysis ----------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", help="base ref (default: PR base, Jenkins last good commit, or HEAD~1)")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--working", action="store_true", help="include uncommitted changes")
    ap.add_argument("--exclude", nargs="*", default=[], help="directory names to skip")
    ap.add_argument("--output", default="analyzer_result.json")
    args = ap.parse_args()

    repo = Path(run(["git", "rev-parse", "--show-toplevel"], args.repo).strip())
    base = args.base or default_base(repo)
    services = find_services(repo, set(args.exclude))
    changes = changed_files(repo, base, args.head, args.working)

    # index every test file in the repo and give it an owner
    tests = []
    for dp, dns, fns in os.walk(repo):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and d not in args.exclude]
        for fn in fns:
            rel = (Path(dp) / fn).relative_to(repo).as_posix()
            if is_test(rel) and Path(fn).suffix in EXT_LANG:
                svc = service_of(rel, services)
                if not svc:
                    svc = next((s for s in services if s["name"] in rel.split("/")), None)
                tests.append({"path": rel, "service": svc["name"] if svc else None,
                              "kind": "integration" if is_integration(rel) else "unit"})

    per_service, shared_changed, run_all_reasons = {}, [], []
    for c in changes:
        c["type"] = classify(c["path"])
        svc = service_of(c["path"], services)
        c["service"] = svc["name"] if svc else None
        if c["type"] in ("ignored", "docs"):
            continue
        if svc:
            per_service.setdefault(svc["name"], []).append(c)
        elif c["type"] in ("source", "config", "other"):
            shared_changed.append(c)
            run_all_reasons.append(f"shared {c['type']} file changed outside any service: {c['path']}")
        elif c["type"] == "test":
            shared_changed.append(c)

    run_all = bool(run_all_reasons)
    svc_by_name = {s["name"]: s for s in services}
    affected = []
    for name, cs in sorted(per_service.items()):
        own = [t for t in tests if t["service"] == name]
        picked, reasons = {}, []
        types = {c["type"] for c in cs}
        if "config" in types or run_all:
            for t in own:
                picked[t["path"]] = t
            reasons.append("config/build file changed -> full service suite")
        if "source" in types:
            stems = {norm(Path(c["path"]).stem) for c in cs if c["type"] == "source"}
            unit = [t for t in own if t["kind"] == "unit"]
            hits = [t for t in unit if any(s and (s in norm(Path(t["path"]).stem) or norm(Path(t["path"]).stem) in s) for s in stems)]
            for t in (hits or unit) + [t for t in own if t["kind"] == "integration"]:
                picked[t["path"]] = t
            reasons.append("source changed -> " + ("name-matched unit tests" if hits else "all unit tests (no name match)") + " + integration tests")
        for c in cs:
            if c["type"] == "test" and c["status"] != "D":
                picked[c["path"]] = next((t for t in own if t["path"] == c["path"]), {"path": c["path"], "kind": "unit"})
        if "test" in types:
            reasons.append("test file changed -> run it")
        affected.append({**svc_by_name[name],
                         "changed_files": [{"path": c["path"], "type": c["type"], "status": c["status"]} for c in cs],
                         "tests_to_run": sorted(picked), "reasons": reasons})

    shared_tests = sorted(t["path"] for t in tests if t["service"] is None)
    if run_all:
        for s in services:
            if s["name"] not in per_service:
                affected.append({**s, "changed_files": [], "tests_to_run": sorted(t["path"] for t in tests if t["service"] == s["name"]),
                                 "reasons": ["shared change -> run everything"]})
    result = {
        "base": base, "head": args.head,
        "run_all": run_all, "run_all_reasons": run_all_reasons,
        "nothing_to_test": not affected and not shared_changed,
        "changed_files": changes,
        "affected_services": affected,
        "shared_tests_to_run": shared_tests if (affected or shared_changed) else [],
        "tests_to_run": sorted({t for a in affected for t in a["tests_to_run"]} | set(shared_tests if affected else [])),
        "summary": f"{len(changes)} changed file(s), {len(affected)} affected service(s)",
    }
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(result["summary"])
    for a in affected:
        print(f"  {a['name']} [{a['language']}]: {len(a['tests_to_run'])} test file(s) -> {a['test_command']}")


if __name__ == "__main__":
    main()
