#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parent


def run(command: list[str], label: str) -> None:
    print(f"\n== {label} ==")
    completed = subprocess.run(command, cwd=REPO)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def check_required() -> None:
    required = [
        REPO / "README.md",
        REPO / "LICENSE",
        REPO / "requirements-validation.txt",
        REPO / ".github/workflows/validate-skill.yml",
        SKILL / "SKILL.md",
        SKILL / "agents/openai.yaml",
        SKILL / "tests/runtime/run-runtime-validation.py",
        SKILL / "tests/runtime/runtime-manifest.json",
        SKILL / "tests/runtime/runtime-report.md",
        SKILL / "tests/runtime/runtime-contact-sheet.svg",
    ]
    missing = [str(path.relative_to(REPO)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing required files:\n" + "\n".join(f"- {item}" for item in missing))


def check_markdown_links() -> None:
    markdown_files = [REPO / "README.md"] + sorted(SKILL.rglob("*.md"))
    broken: list[str] = []
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for doc in markdown_files:
        text = doc.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "sandbox:")):
                continue
            target = target.replace("%20", " ")
            resolved = (doc.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{doc.relative_to(REPO)} -> {target}")
    if broken:
        raise SystemExit("Broken relative links:\n" + "\n".join(f"- {item}" for item in broken))
    print(f"Markdown links checked: {len(markdown_files)} files")


def check_runtime_manifest() -> None:
    manifest = json.loads((SKILL / "tests/runtime/runtime-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("skill_name") != "machinery-card-generator":
        raise SystemExit("Runtime manifest has wrong skill_name")
    cases = manifest.get("cases", [])
    ids = {case.get("id") for case in cases}
    expected = {"real-bulldozer", "toy-loader", "child-road-roller", "unclear-object"}
    if ids != expected:
        raise SystemExit(f"Runtime manifest cases mismatch: {sorted(ids)}")
    generated = [case for case in cases if case.get("decision") == "generate"]
    stopped = [case for case in cases if case.get("decision") == "stop_before_generation"]
    if len(generated) != 3 or len(stopped) != 1:
        raise SystemExit("Runtime manifest must contain 3 generated cases and 1 stop case")
    for case in generated:
        if case.get("scene_machine_name") == case.get("right_title"):
            raise SystemExit(f"{case['id']}: left and right names are equal")
        if case.get("critical_errors"):
            raise SystemExit(f"{case['id']}: critical errors remain")
        for flag in ("analysis_visible_before_generation", "data_locked_before_generation", "final_image_exists", "final_image_opened", "final_image_attached_contract"):
            if case.get(flag) is not True:
                raise SystemExit(f"{case['id']}: {flag} is not true")
    stop_case = stopped[0]
    if stop_case.get("generation_started") is not False or stop_case.get("clarification_requested") is not True:
        raise SystemExit("Unclear object does not stop before generation")
    print("Runtime manifest contract passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the complete tech-card-generator validation gate")
    parser.add_argument("--skip-runtime", action="store_true", help="Skip deterministic runtime generation; intended only for diagnostics")
    args = parser.parse_args()
    check_required()
    run([sys.executable, str(SKILL / "scripts/validate-agent-skills-spec.py"), str(SKILL)], "Agent Skills specification")
    run([sys.executable, str(SKILL / "scripts/validate-content.py")], "Skill content")
    check_runtime_manifest()
    check_markdown_links()
    if not args.skip_runtime:
        with tempfile.TemporaryDirectory(prefix="tech-card-generator-gate-") as tmp:
            run([sys.executable, str(SKILL / "tests/runtime/run-runtime-validation.py"), "--output-dir", tmp], "Runtime contract harness")
    print("\nRepository validation gate passed")


if __name__ == "__main__":
    main()
