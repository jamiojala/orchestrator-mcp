import asyncio
import json
from pathlib import Path

from orchestrator_mcp.server import build_server


def _extract_tool_map(server: object) -> dict[str, object]:
    for attribute in ("_tool_manager", "tool_manager"):
        manager = getattr(server, attribute, None)
        if manager is None:
            continue
        for name in ("_tools", "tools"):
            tools = getattr(manager, name, None)
            if isinstance(tools, dict):
                return tools
    raise AssertionError("Could not locate FastMCP tool registry for smoke testing")


def test_server_registers_expected_tools(tmp_path: Path) -> None:
    server = build_server(tmp_path / "missing-config.yaml")
    tools = _extract_tool_map(server)
    assert "estimate_complexity" in tools
    assert "llm_list_providers" in tools
    assert "skill_marketplace_list" in tools


def test_estimate_complexity_tool_is_callable(tmp_path: Path) -> None:
    server = build_server(tmp_path / "missing-config.yaml")
    tools = _extract_tool_map(server)
    tool = tools["estimate_complexity"]
    result = asyncio.run(tool.fn({"task": "Fix a small bug", "file_count": 1, "estimated_changed_lines": 20}))
    payload = json.loads(result)
    assert payload["complexity_score"] >= 1
