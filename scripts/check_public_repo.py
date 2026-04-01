#!/usr/bin/env python3
"""Check the repo for obvious secrets and local-only references before publishing."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from orchestrator_mcp.safety import scan_public_release_tree


def main() -> int:
    findings = scan_public_release_tree(REPO_ROOT)
    if findings:
        print("Public release scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public release scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
