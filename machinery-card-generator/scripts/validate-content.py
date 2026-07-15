#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

required_files = [
    "SKILL.md",
    "references/analysis-rules.md",
    "references/style-lock.md",
    "references/card-layout.md",
    "references/output-template.md",
    "references/quality-check.md",
    "agents/openai.yaml",
    "examples/tracked-bulldozer.md",
    "examples/toy-bulldozer.md",
    "examples/child-sketch.md",
    "examples/unclear-object.md",
    "tests/cases.yaml",
    "tests/dry-run-real-bulldozer.md",
]

for rel in required_files:
    if not (ROOT / rel).is_file():
        errors.append(f"Отсутствует обязательный файл: {rel}")

for forbidden in ["README.md", "CHANGELOG.md", "CHANGELOG"]:
    if (ROOT / forbidden).exists():
        errors.append(f"Обнаружен лишний документ: {forbidden}")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
analysis = (ROOT / "references/analysis-rules.md").read_text(encoding="utf-8")
style = (ROOT / "references/style-lock.md").read_text(encoding="utf-8")
layout = (ROOT / "references/card-layout.md").read_text(encoding="utf-8")
template = (ROOT / "references/output-template.md").read_text(encoding="utf-8")
quality = (ROOT / "references/quality-check.md").read_text(encoding="utf-8")
bulldozer = (ROOT / "examples/tracked-bulldozer.md").read_text(encoding="utf-8")
dry_run = (ROOT / "tests/dry-run-real-bulldozer.md").read_text(encoding="utf-8")

frontmatter_match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
if not frontmatter_match:
    errors.append("SKILL.md не содержит корректный YAML frontmatter")
else:
    data = yaml.safe_load(frontmatter_match.group(1))
    if data.get("name") != "machinery-card-generator":
        errors.append("Имя навыка изменено")
    if not data.get("description"):
        errors.append("Отсутствует description")
    if data.get("metadata", {}).get("version") != "2.1.0":
        errors.append("Версия навыка должна быть 2.1.0")

openai = yaml.safe_load((ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
interface = openai.get("interface", {})
if not interface.get("display_name"):
    errors.append("agents/openai.yaml: отсутствует interface.display_name")
if "прикреп" not in interface.get("default_prompt", "").lower():
    errors.append("agents/openai.yaml: default_prompt не требует прикрепить изображение")
if openai.get("policy", {}).get("allow_implicit_invocation") is not True:
    errors.append("agents/openai.yaml: allow_implicit_invocation должен быть true")

required_stage_markers = [
    "### 1. Определи тип исходного материала",
    "### 2. Выбери ровно одну главную машину",
    "### 3. Определи характер изображения",
    "### 4. При необходимости выбери один реальный аналог",
    "### 5. Проведи полный анализ",
    "### 6. Подготовь четыре варианта названия машины",
    "### 7. Выбери разные варианты названия для левого и правого блоков",
    "### 8. Подготовь четыре точных текста карточки",
    "### 9. Покажи пользователю полный анализ и точные тексты до генерации",
    "### 10. Выполни предгенерационную проверку",
    "### 11. Зафиксируй все данные",
    "### 12. Сформируй генерационный промпт только из зафиксированных данных",
    "### 13. Создай изображение",
    "### 14. Определи актуальный путь созданного файла",
    "### 15. Проверь существование и доступность файла",
    "### 16. Открой изображение и проведи полную визуальную проверку",
    "### 17. При критической ошибке исправь только соответствующую часть промпта",
    "### 18. Повторяй проверку до устранения всех критических ошибок",
    "### 19. Прикрепи последнюю прошедшую проверку версию к финальному ответу",
    "### 20. Убедись, что изображение отображается непосредственно пользователю",
    "### 21. Только после этого считай задачу завершённой",
]
for marker in required_stage_markers:
    if marker not in skill:
        errors.append(f"SKILL.md: отсутствует этап: {marker}")

for rel in [
    "references/analysis-rules.md",
    "references/style-lock.md",
    "references/card-layout.md",
    "references/output-template.md",
    "references/quality-check.md",
]:
    if rel not in skill:
        errors.append(f"SKILL.md: отсутствует ссылка на {rel}")
    if not (ROOT / rel).is_file():
        errors.append(f"Внутренняя ссылка ведёт на отсутствующий файл: {rel}")

required_fields = [
    "source_type", "source_character", "source_observations",
    "selected_machine_reason", "visible_evidence", "unknowns", "assumptions",
    "real_analogue_status", "real_analogue_class", "analogue_evidence",
    "analogue_confidence", "source_distortions", "analogue_differences",
    "excluded_source_features", "title_name_1", "title_name_2", "title_name_3",
    "title_name_4", "scene_machine_name", "right_title", "name_choice_rationale",
    "names_differ_check", "precise_name", "confidence", "key_feature",
    "key_function", "working_element", "child_element_name", "how_it_works",
    "action_start_state", "working_element_position", "material_interaction",
    "visible_action_result", "action_readability_evidence",
    "action_readable_without_text", "typical_environment",
    "best_use_environment", "effective_work", "task_1_name", "task_1_description",
    "task_2_name", "task_2_description", "task_3_name", "task_3_description",
    "primary_task", "environment_description", "background_description",
    "plot_rationale", "scene_title", "child_task_text",
]
for field in required_fields:
    if f"`{field}`" not in analysis:
        errors.append(f"analysis-rules.md: отсутствует поле {field}")

for deprecated in ["short_name", "70–80", "70-80%", "70–80%"]:
    for name, text in {
        "SKILL.md": skill,
        "analysis-rules.md": analysis,
        "style-lock.md": style,
        "card-layout.md": layout,
        "output-template.md": template,
        "quality-check.md": quality,
    }.items():
        if deprecated in text:
            errors.append(f"{name}: сохранилось устаревшее правило или поле '{deprecated}'")

analysis_phrases = [
    "Да, названия машины слева и справа различаются не только действием",
    "Можно ли без текста однозначно понять, что именно делает машина?",
    "передний план",
    "средний план",
    "дальний план",
]
for phrase in analysis_phrases:
    if phrase.lower() not in analysis.lower():
        errors.append(f"analysis-rules.md: отсутствует правило: {phrase}")

style_phrases = [
    "Почти пустое окружение запрещено",
    "передний план",
    "средний план",
    "дальний план",
    "примерно на 20–35% светлее и проще",
    "зона не уничтожает передний, средний или дальний план",
    "Статичная демонстрационная поза",
]
for phrase in style_phrases:
    if phrase.lower() not in style.lower():
        errors.append(f"style-lock.md: отсутствует правило: {phrase}")

layout_phrases = [
    "50–60% безопасной области",
    "не превышает 65% безопасной области",
    "не превышает 60% безопасной области",
    "не менее 30% визуально доступной площади",
    "передний план",
    "средний план",
    "дальний план",
    "`scene_title`",
    "`right_title`",
    "Одинаковое название машины слева и справа является критической ошибкой",
    "запрет на пустой студийный фон",
]
for phrase in layout_phrases:
    if phrase.lower() not in layout.lower():
        errors.append(f"card-layout.md: отсутствует правило: {phrase}")

required_template_sections = [
    "## Часть 1. Видимый предгенерационный результат",
    "# Тип исходного материала",
    "# Что дано пользователем",
    "# Что за техника",
    "# Почему выбрана эта машина",
    "# Что видно на исходном изображении",
    "# Реальный аналог",
    "# Что нельзя определить",
    "# Ключевая особенность",
    "# Как машина работает",
    "# Рабочая среда",
    "# Три реальные задачи",
    "# Главный сюжет",
    "# Подробное окружение",
    "# Допустимый фон",
    "# Почему выбран этот сюжет",
    "# Точные тексты карточки",
    "# Навык применён полностью",
    "## Часть 2. Финальная пользовательская выдача",
]
for section in required_template_sections:
    if section not in template:
        errors.append(f"output-template.md: отсутствует раздел {section}")

for placeholder in [
    "{scene_machine_name}", "{right_title}", "{action_start_state}",
    "{working_element_position}", "{material_interaction}",
    "{visible_action_result}", "{action_readability_evidence}",
    "{environment_description}", "{scene_title}", "{child_task_text}",
    "{child_element_name}",
]:
    if placeholder not in template:
        errors.append(f"output-template.md: отсутствует плейсхолдер {placeholder}")

final_template = "![Готовая образовательная карточка](sandbox:{final_image_path})"
if final_template not in template:
    errors.append("output-template.md: отсутствует обязательный финальный шаблон изображения")
for phrase in [
    "плейсхолдер не может остаться",
    "после изображения ничего не добавляется",
    "изображение должно отображаться непосредственно",
]:
    if phrase.lower() not in template.lower():
        errors.append(f"output-template.md: отсутствует правило пользовательской выдачи: {phrase}")

quality_phrases = [
    "машина занимает примерно 50–60% безопасной области",
    "окружение занимает не менее 30%",
    "передний, средний и дальний планы",
    "рабочая часть взаимодействует с материалом",
    "точка контакта видна",
    "задача определяется без чтения подписи",
    "слева и справа используется одинаковое название машины",
    "полный анализ не показан пользователю до генерации",
    "изображение создано, но не прикреплено",
    "финальный ответ пустой",
    "использован несуществующий, временный или устаревший путь",
    "после финального изображения добавлен лишний текст",
    "Проверка пользовательской выдачи",
]
for phrase in quality_phrases:
    if phrase.lower() not in quality.lower():
        errors.append(f"quality-check.md: отсутствует проверка: {phrase}")

exact_bulldozer_texts = [
    "Гусеничный бульдозер разравнивает землю",
    "Бульдозер",
    "Бульдозер толкает землю большим щитом. Земля становится ровной.",
    "Широкий щит",
]
for phrase in exact_bulldozer_texts:
    if phrase not in bulldozer:
        errors.append(f"Пример бульдозера: отсутствует точный текст: {phrase}")
    if phrase not in dry_run:
        errors.append(f"Сухой прогон бульдозера: отсутствует точный текст: {phrase}")

for field in [
    "scene_machine_name", "right_title", "action_start_state",
    "working_element_position", "material_interaction", "visible_action_result",
    "action_readability_evidence", "action_readable_without_text",
]:
    if f"`{field}`" not in bulldozer and f"**{field}" not in dry_run:
        errors.append(f"Практический пример: отсутствует поле {field}")

child_text_match = re.search(r"`child_task_text`: (.+)", bulldozer)
if not child_text_match:
    errors.append("Пример бульдозера: не найден child_task_text")
elif "отвал" in child_text_match.group(1).lower():
    errors.append("Пример бульдозера: слово 'отвал' попало в детский текст")

child_element_match = re.search(r"`child_element_name`: (.+)", bulldozer)
if not child_element_match:
    errors.append("Пример бульдозера: не найден child_element_name")
elif "отвал" in child_element_match.group(1).lower():
    errors.append("Пример бульдозера: слово 'отвал' попало в подпись детали")

cases = yaml.safe_load((ROOT / "tests/cases.yaml").read_text(encoding="utf-8"))
ids = {case["id"] for case in cases.get("cases", [])}
for expected in {"real-bulldozer", "toy-construction-machine", "child-sketch", "unclear-object"}:
    if expected not in ids:
        errors.append(f"tests/cases.yaml: отсутствует сценарий {expected}")
real_case = next((case for case in cases.get("cases", []) if case.get("id") == "real-bulldozer"), {})
if real_case.get("expected_scene_machine_name") == real_case.get("expected_right_title"):
    errors.append("tests/cases.yaml: названия слева и справа совпадают")
if real_case.get("expected_environment_min_percent") != 30:
    errors.append("tests/cases.yaml: минимальная доля окружения должна быть 30%")
if real_case.get("final_image_must_be_attached") is not True:
    errors.append("tests/cases.yaml: не зафиксировано обязательное прикрепление изображения")

unclear = (ROOT / "examples/unclear-object.md").read_text(encoding="utf-8")
for phrase in ["запросить", "генерация изображения не начинается"]:
    if phrase.lower() not in unclear.lower():
        errors.append(f"Неясный объект: отсутствует поведение '{phrase}'")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Проверка завершена: {len(errors)} ошибок")
    sys.exit(1)

print("Проверка содержательных требований пройдена")
print(f"Проверено обязательных файлов: {len(required_files)}")
print("Проверено этапов выполнения: 21")
print(f"Проверено обязательных полей: {len(required_fields)}")
print("Проверено сценариев: 4")
