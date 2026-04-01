"""Skill manifest loading and matching."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in minimal environments
    yaml = None  # type: ignore[assignment]

from .models import SkillManifestModel, TaskType


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def _parse_scalar(value: str) -> object:
    cleaned = value.strip()
    if cleaned in {"true", "True"}:
        return True
    if cleaned in {"false", "False"}:
        return False
    if cleaned.startswith("[") and cleaned.endswith("]"):
        inner = cleaned[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",")]
    return cleaned.strip("'\"")


def _parse_frontmatter_without_yaml(text: str) -> dict[str, object]:
    parsed: dict[str, object] = {}
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("  "):
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if value == "|":
            index += 1
            block: list[str] = []
            while index < len(lines):
                child = lines[index]
                if child.startswith("  "):
                    block.append(child[2:])
                    index += 1
                    continue
                if not child.strip():
                    block.append("")
                    index += 1
                    continue
                break
            parsed[key] = "\n".join(block).rstrip()
            continue

        if not value:
            index += 1
            items: list[object] = []
            while index < len(lines):
                child = lines[index]
                if child.startswith("  - "):
                    items.append(_parse_scalar(child[4:]))
                    index += 1
                    continue
                if not child.strip():
                    index += 1
                    continue
                break
            parsed[key] = items
            continue

        parsed[key] = _parse_scalar(value)
        index += 1

    return parsed


class SkillRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._skills: dict[str, SkillManifestModel] = {}

    def load(self) -> dict[str, SkillManifestModel]:
        skills: dict[str, SkillManifestModel] = {}
        if self.root.exists():
            for skill_dir in sorted(path for path in self.root.iterdir() if path.is_dir()):
                manifest = self._load_skill(skill_dir)
                if manifest is not None:
                    skills[manifest.slug] = manifest
        self._skills = skills
        return skills

    def _load_skill(self, skill_dir: Path) -> SkillManifestModel | None:
        yaml_path = skill_dir / "skill.yaml"
        markdown_path = skill_dir / "SKILL.md"
        if yaml_path.exists() and yaml is not None:
            raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            return SkillManifestModel.model_validate(raw)
        if markdown_path.exists():
            return self._load_markdown_skill(markdown_path)
        return None

    def _load_markdown_skill(self, markdown_path: Path) -> SkillManifestModel | None:
        text = markdown_path.read_text(encoding="utf-8")
        match = FRONTMATTER_PATTERN.match(text)
        if match is None:
            return None
        frontmatter = (yaml.safe_load(match.group(1)) if yaml is not None else _parse_frontmatter_without_yaml(match.group(1))) or {}
        body = match.group(2).strip()
        if not isinstance(frontmatter, dict):
            return None
        triggers = frontmatter.pop("triggers", {}) or {}
        keywords = frontmatter.pop("keywords", None)
        file_globs = frontmatter.pop("file_globs", None)
        task_types = frontmatter.pop("task_types", None)
        if keywords is not None:
            triggers["keywords"] = keywords
        if file_globs is not None:
            triggers["file_globs"] = file_globs
        if task_types is not None:
            triggers["task_types"] = task_types
        synthesized = {
            "slug": markdown_path.parent.name,
            "name": frontmatter.get("name", markdown_path.parent.name.replace("-", " ").title()),
            "description": frontmatter.get("description", body.splitlines()[0] if body else "Portable skill pack"),
            "public": frontmatter.get("public", True),
            "category": frontmatter.get("category"),
            "tags": frontmatter.get("tags", []),
            "preferred_models": frontmatter.get("preferred_models", []),
            "prompt_template": frontmatter.get("prompt_template", body or "See SKILL.md"),
            "validation": frontmatter.get("validation", []),
            "triggers": triggers,
        }
        return SkillManifestModel.model_validate(synthesized)

    def all(self) -> list[SkillManifestModel]:
        if not self._skills:
            self.load()
        return list(self._skills.values())

    def get(self, slug: str) -> SkillManifestModel | None:
        if not self._skills:
            self.load()
        return self._skills.get(slug)

    def match(
        self,
        task_text: str,
        task_type: TaskType,
        file_paths: list[str] | None = None,
    ) -> list[SkillManifestModel]:
        if not self._skills:
            self.load()
        lowered = task_text.lower()
        matches: list[SkillManifestModel] = []
        for skill in self._skills.values():
            keyword_match = any(keyword.lower() in lowered for keyword in skill.triggers.keywords)
            task_type_match = not skill.triggers.task_types or task_type.value in skill.triggers.task_types
            file_match = False
            if file_paths and skill.triggers.file_globs:
                for file_path in file_paths:
                    if any(Path(file_path).match(pattern) for pattern in skill.triggers.file_globs):
                        file_match = True
                        break
            if (keyword_match or file_match) and task_type_match:
                matches.append(skill)
        return matches

    def summary(self) -> list[dict[str, object]]:
        return [
            {
                "slug": skill.slug,
                "name": skill.name,
                "public": skill.public,
                "category": skill.category,
                "tags": skill.tags,
                "preferred_models": skill.preferred_models,
                "validation": skill.validation,
            }
            for skill in self.all()
        ]
