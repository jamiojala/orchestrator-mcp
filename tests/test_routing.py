from orchestrator_mcp.models import ComplexityInput, TaskType, WorkMode
from orchestrator_mcp.routing import build_complexity_payload, choose_mode


def test_choose_mode_prefers_orchestrator_for_large_changes() -> None:
    mode, reasons, score = choose_mode(
        ComplexityInput(
            task="Build a full page with new architecture and animation",
            task_type=TaskType.ARCHITECTURE,
            file_count=6,
            estimated_changed_lines=900,
            needs_architecture=True,
            needs_animation=True,
        )
    )
    assert mode == WorkMode.ORCHESTRATOR
    assert score >= 7
    assert reasons


def test_build_complexity_payload_reports_mode() -> None:
    payload = build_complexity_payload(ComplexityInput(task="Fix a small type error", file_count=1, estimated_changed_lines=20))
    assert payload["recommended_mode"] in {WorkMode.ENGINEER.value, WorkMode.ORCHESTRATOR.value}
