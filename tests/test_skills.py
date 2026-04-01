from pathlib import Path

from orchestrator_mcp.skills import SkillRegistry


def test_skill_registry_loads_markdown_frontmatter(tmp_path: Path) -> None:
    skill_dir = tmp_path / "portable-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        """---
name: Portable Skill
description: Portable skill for testing.
public: true
category: testing
tags: [portable]
preferred_models:
  - gemini-2.5-flash
validation:
  - verify_text_unchanged
keywords: [portable]
task_types: [review]
prompt_template: |
  Test prompt template.
---
# Portable Skill
Body
""",
        encoding="utf-8",
    )
    registry = SkillRegistry(tmp_path)
    loaded = registry.load()
    assert "portable-skill" in loaded
    assert loaded["portable-skill"].category == "testing"
