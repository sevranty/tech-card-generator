#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "machinery-card-generator"
DIST = REPO / "dist"

INCLUDE = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/analysis-rules.md",
    "references/style-lock.md",
    "references/card-layout.md",
    "references/output-template.md",
    "references/quality-check.md",
    "examples/tracked-bulldozer.md",
    "examples/toy-bulldozer.md",
    "examples/child-sketch.md",
    "examples/unclear-object.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version() -> str:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*["\']([^"\']+)["\']', text, re.M)
    if not match:
        raise SystemExit("SKILL.md metadata.version not found")
    return match.group(1)


def build(out_dir: Path) -> tuple[Path, Path, Path]:
    ver = version()
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"machinery-card-generator-v{ver}.zip"
    checksum = out_dir / f"machinery-card-generator-v{ver}.sha256"
    manifest_path = out_dir / "release-manifest.json"

    missing = [rel for rel in INCLUDE if not (SKILL / rel).is_file()]
    if missing:
        raise SystemExit("Missing package files: " + ", ".join(missing))

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in sorted(INCLUDE):
            source = SKILL / rel
            info = zipfile.ZipInfo(f"machinery-card-generator/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, source.read_bytes())

    digest = sha256(archive)
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    files = []
    for rel in sorted(INCLUDE):
        source = SKILL / rel
        files.append({"path": f"machinery-card-generator/{rel}", "size": source.stat().st_size, "sha256": sha256(source)})
    manifest = {
        "schema_version": "1.0",
        "skill_name": "machinery-card-generator",
        "version": ver,
        "archive": archive.name,
        "archive_size": archive.stat().st_size,
        "archive_sha256": digest,
        "root_directory": "machinery-card-generator/",
        "file_count": len(files),
        "files": files,
        "excluded_repository_only": ["tests/", "scripts/", "generated evidence", "README.md", "CHANGELOG.md"],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="tcg-release-check-") as tmp:
        target = Path(tmp)
        with zipfile.ZipFile(archive) as zf:
            bad = zf.testzip()
            if bad:
                raise SystemExit(f"Corrupt archive member: {bad}")
            zf.extractall(target)
        extracted = target / "machinery-card-generator"
        if not extracted.is_dir():
            raise SystemExit("Archive root directory is invalid")
        subprocess.run([sys.executable, str(SKILL / "scripts/validate-agent-skills-spec.py"), str(extracted)], check=True)
        for rel in INCLUDE:
            if not (extracted / rel).is_file():
                raise SystemExit(f"Extracted file missing: {rel}")

    print(f"Release package built: {archive.name}")
    print(f"SHA-256: {digest}")
    print(f"Files: {len(INCLUDE)}")
    return archive, checksum, manifest_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DIST)
    args = parser.parse_args()
    build(args.output_dir.resolve())


if __name__ == "__main__":
    main()
