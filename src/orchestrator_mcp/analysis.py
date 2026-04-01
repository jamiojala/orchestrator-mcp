"""Diff, design, text, and safe git-analysis helpers."""

from __future__ import annotations

import difflib
from collections import Counter
from typing import Any


def normalize_text(value: str, normalize_whitespace: bool, ignore_case: bool) -> str:
    normalized = value
    if normalize_whitespace:
        normalized = "\n".join(line.strip() for line in normalized.splitlines()).strip()
        normalized = " ".join(normalized.split())
    if ignore_case:
        normalized = normalized.lower()
    return normalized


def generate_diff_text(original: str, revised: str, path: str, context_lines: int) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        revised.splitlines(),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        n=context_lines,
        lineterm="",
    )
    return "\n".join(diff)


def verify_text_unchanged_payload(
    original: str,
    candidate: str,
    normalize_whitespace: bool,
    ignore_case: bool,
) -> dict[str, Any]:
    normalized_original = normalize_text(original, normalize_whitespace, ignore_case)
    normalized_candidate = normalize_text(candidate, normalize_whitespace, ignore_case)
    identical = normalized_original == normalized_candidate
    preview = list(
        difflib.unified_diff(
            normalized_original.splitlines(),
            normalized_candidate.splitlines(),
            fromfile="original",
            tofile="candidate",
            n=1,
            lineterm="",
        )
    )
    return {
        "identical": identical,
        "normalize_whitespace": normalize_whitespace,
        "ignore_case": ignore_case,
        "diff_line_count": len(preview),
        "preview": preview[:20],
    }


def design_audit_payload(code: str, profile: str) -> dict[str, Any]:
    lowered = code.lower()
    issues: list[dict[str, str]] = []
    checks: list[dict[str, Any]] = []

    has_em_dash = "—" in code
    checks.append({"name": "forbidden_em_dash", "passed": not has_em_dash})
    if has_em_dash:
        issues.append({"severity": "error", "rule": "forbidden_em_dash", "message": "Found an em-dash. Use hyphens or colons instead."})

    has_blur = "backdrop-blur" in lowered
    checks.append({"name": "glass_blur_present", "passed": has_blur})
    if not has_blur:
        issues.append({"severity": "warning", "rule": "glass_blur_present", "message": "No backdrop blur token found."})

    has_glass_tint = any(token in lowered for token in ["bg-white/5", "bg-white/10", "border-white/10", "border-white/20"])
    checks.append({"name": "glass_tint_tokens", "passed": has_glass_tint})
    if not has_glass_tint:
        issues.append({"severity": "warning", "rule": "glass_tint_tokens", "message": "No translucent glass tint tokens found."})

    uses_pure_black = any(token in lowered for token in ["#000", "#000000", "bg-black", "text-black"])
    checks.append({"name": "avoid_pure_black", "passed": not uses_pure_black})
    if uses_pure_black:
        issues.append({"severity": "warning", "rule": "avoid_pure_black", "message": "Found pure black usage in a premium visual profile."})

    risky_animation_lines: list[str] = []
    risky_tokens = ["left:", "top:", "width:", "height:", "margin-left", "margin-top", "padding:"]
    for raw_line in code.splitlines():
        line = raw_line.strip().lower()
        if "animate" in line or "transition" in line or "motion" in line:
            if any(token in line for token in risky_tokens):
                risky_animation_lines.append(raw_line.strip())

    checks.append({"name": "gpu_friendly_animation", "passed": not risky_animation_lines})
    if risky_animation_lines:
        issues.append({"severity": "warning", "rule": "gpu_friendly_animation", "message": "Found animation lines that may cause layout thrashing."})

    return {
        "profile": profile,
        "passed": not any(issue["severity"] == "error" for issue in issues),
        "checks": checks,
        "issues": issues,
        "risky_animation_lines": risky_animation_lines[:10],
    }


def summarize_unified_diff(diff_text: str) -> dict[str, Any]:
    files: list[str] = []
    added = 0
    removed = 0
    file_counter: Counter[str] = Counter()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line.replace("+++ b/", "", 1)
            files.append(path)
            file_counter[path] += 1
        elif line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return {
        "files": files,
        "file_count": len(files),
        "added_lines": added,
        "removed_lines": removed,
        "file_extensions": Counter(path.split(".")[-1] if "." in path else "none" for path in files),
        "top_files": list(file_counter.keys())[:5],
    }


def _classify_change(summary: dict[str, Any]) -> str:
    files = summary["files"]
    if files and all(path.endswith(".md") for path in files):
        return "docs"
    if any(path.startswith("tests/") or path.endswith("_test.py") or path.startswith("test_") for path in files):
        return "test"
    if any(path.endswith((".py", ".tsx", ".ts", ".js", ".jsx")) for path in files):
        if summary["added_lines"] > summary["removed_lines"]:
            return "feat"
        return "refactor"
    return "chore"


def git_commit_message_payload(diff_text: str, context: str | None = None) -> dict[str, Any]:
    summary = summarize_unified_diff(diff_text)
    change_type = _classify_change(summary)
    subject = {
        "docs": "document orchestrator workflows and setup",
        "test": "expand orchestration coverage",
        "feat": "add orchestrator platform foundations",
        "refactor": "refactor orchestration internals",
        "chore": "update orchestrator project scaffolding",
    }[change_type]
    if context:
        subject = f"{subject} for {context.strip().lower()}"
    return {
        "type": change_type,
        "subject": subject,
        "conventional_commit": f"{change_type}: {subject}",
        "summary": summary,
    }


def git_pr_description_payload(diff_text: str, context: str | None = None) -> dict[str, Any]:
    summary = summarize_unified_diff(diff_text)
    headline = context.strip() if context else "Introduce the first public orchestrator-mcp beta foundation"
    body = "\n".join(
        [
            f"## What changed\n- Updated {summary['file_count']} files",
            f"- Added {summary['added_lines']} lines and removed {summary['removed_lines']} lines",
            f"- Main files: {', '.join(summary['top_files']) if summary['top_files'] else 'n/a'}",
            "",
            "## Why",
            f"- {headline}",
            "",
            "## Validation",
            "- Run package smoke tests",
            "- Check safety scan",
            "- Verify docs and entrypoints",
        ]
    )
    return {"title": headline, "body": body, "summary": summary}


def git_code_review_payload(diff_text: str, context: str | None = None) -> dict[str, Any]:
    summary = summarize_unified_diff(diff_text)
    findings: list[dict[str, str]] = []
    lowered = diff_text.lower()
    if "api_key" in lowered or "secret" in lowered or "nvapi-" in lowered or "aiza" in lowered:
        findings.append({"severity": "high", "message": "Diff appears to contain secret-like material. Verify redaction and environment-only configuration."})
    if summary["file_count"] > 0 and not any(path.startswith("tests/") for path in summary["files"]):
        findings.append({"severity": "medium", "message": "No test files changed. Confirm whether coverage is sufficient for this change."})
    if any(path.endswith(".md") for path in summary["files"]) and not any(path.startswith("docs/") for path in summary["files"]):
        findings.append({"severity": "low", "message": "Documentation changed outside the docs site. Check for duplication or drift."})
    return {
        "context": context,
        "summary": summary,
        "findings": findings,
        "approved": not any(item["severity"] == "high" for item in findings),
    }

