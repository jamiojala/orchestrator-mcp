from orchestrator_mcp.analysis import design_audit_payload, generate_diff_text, verify_text_unchanged_payload


def test_generate_diff_text_includes_path_headers() -> None:
    diff = generate_diff_text("a\n", "b\n", "demo.txt", 3)
    assert "a/demo.txt" in diff
    assert "b/demo.txt" in diff


def test_verify_text_unchanged_detects_equivalent_text() -> None:
    payload = verify_text_unchanged_payload("Hello world", "Hello   world", True, False)
    assert payload["identical"] is True


def test_design_audit_flags_em_dash() -> None:
    payload = design_audit_payload("const copy = 'bad — token';", "liquid_glass")
    assert payload["passed"] is False
    assert any(issue["rule"] == "forbidden_em_dash" for issue in payload["issues"])
