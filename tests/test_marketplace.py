from pathlib import Path

from orchestrator_mcp.marketplace import export_skill_pack, get_marketplace_skill, list_marketplace_skills


def test_marketplace_contains_expected_skill_count() -> None:
    skills = list_marketplace_skills()
    assert len(skills) == 100


def test_marketplace_lookup_returns_featured_skill() -> None:
    skill = get_marketplace_skill("liquid-glass-enforcer")
    assert skill is not None
    assert skill.featured is True


def test_export_skill_pack_writes_portable_files(tmp_path: Path) -> None:
    skill = get_marketplace_skill("liquid-glass-enforcer")
    assert skill is not None
    destination = export_skill_pack(skill, tmp_path)
    assert destination.exists()
    assert (destination / "README.md").exists()
    assert (destination / "SKILL.md").exists()
    assert (destination / "skill.yaml").exists()
    assert (destination / "marketplace.yaml").exists()
