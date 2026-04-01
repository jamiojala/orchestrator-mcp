# Security Policy

## What this project is meant to do

`orchestrator-mcp` is designed to:

- route prompts across configured LLM providers
- redact obvious secrets before outbound calls
- block clearly malicious exfiltration or malware-style requests
- provide non-mutating analysis helpers for diffs, copy preservation, and design checks

It is intentionally not a shell runner, filesystem crawler, or arbitrary code execution system.

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub Security Advisories or another private maintainer channel. Do not open public issues for security-sensitive findings.

Include:

- affected version or commit
- reproduction steps
- expected behavior
- actual behavior
- whether secrets, prompts, or arbitrary execution are at risk

## Secure usage guidance

- keep provider credentials in environment variables only
- do not commit `.env`, editor auth files, caches, or logs
- run `python scripts/check_public_repo.py` before publishing a fork or release
- treat redaction and prompt blocking as defense-in-depth, not absolute guarantees
