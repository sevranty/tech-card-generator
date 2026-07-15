#!/usr/bin/env python3
"""Проверка frontmatter по опубликованным правилам Agent Skills / skills-ref."""
from pathlib import Path
import sys
import unicodedata
import yaml

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        raise ValueError("SKILL.md должен начинаться с YAML frontmatter (---)")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("YAML frontmatter не закрыт разделителем ---")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError("YAML frontmatter должен быть отображением ключ-значение")
    return metadata


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = Path(skill_dir)
    if not skill_dir.exists():
        return [f"Путь не существует: {skill_dir}"]
    if not skill_dir.is_dir():
        return [f"Путь не является папкой: {skill_dir}"]
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["Отсутствует обязательный файл: SKILL.md"]
    try:
        metadata = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except Exception as exc:
        return [str(exc)]

    extra_fields = set(metadata) - ALLOWED_FIELDS
    if extra_fields:
        errors.append(
            "Неожиданные поля frontmatter: " + ", ".join(sorted(extra_fields))
        )

    if "name" not in metadata:
        errors.append("Отсутствует обязательное поле frontmatter: name")
    else:
        name = metadata["name"]
        if not isinstance(name, str) or not name.strip():
            errors.append("Поле name должно быть непустой строкой")
        else:
            name = unicodedata.normalize("NFKC", name.strip())
            if len(name) > MAX_SKILL_NAME_LENGTH:
                errors.append("Имя навыка превышает 64 символа")
            if name != name.lower():
                errors.append("Имя навыка должно быть в нижнем регистре")
            if name.startswith("-") or name.endswith("-"):
                errors.append("Имя не может начинаться или заканчиваться дефисом")
            if "--" in name:
                errors.append("Имя не может содержать два дефиса подряд")
            if not all(char.isalnum() or char == "-" for char in name):
                errors.append("Имя содержит недопустимые символы")
            if skill_dir.name != name:
                errors.append(
                    f"Имя папки '{skill_dir.name}' не совпадает с именем навыка '{name}'"
                )

    if "description" not in metadata:
        errors.append("Отсутствует обязательное поле frontmatter: description")
    else:
        description = metadata["description"]
        if not isinstance(description, str) or not description.strip():
            errors.append("Поле description должно быть непустой строкой")
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append("Описание превышает 1024 символа")

    if "compatibility" in metadata:
        compatibility = metadata["compatibility"]
        if not isinstance(compatibility, str):
            errors.append("Поле compatibility должно быть строкой")
        elif len(compatibility) > MAX_COMPATIBILITY_LENGTH:
            errors.append("Поле compatibility превышает 500 символов")

    return errors


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    problems = validate(target)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        sys.exit(1)
    print("Agent Skills specification validation passed")
