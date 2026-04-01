"""Streamlit observability dashboard."""

from __future__ import annotations

from pathlib import Path

from .config import load_project_config
from .state import StateStore


def render_dashboard(config_path: str | None = None) -> None:
    import streamlit as st

    config = load_project_config(Path(config_path) if config_path else None)
    store = StateStore(config.state_dir / "orchestrator-mcp.sqlite3")

    st.set_page_config(page_title="orchestrator-mcp dashboard", layout="wide")
    st.title("orchestrator-mcp dashboard")
    st.caption("Observe multi-LLM routing, cache hits, model success, and budget burn.")

    recent_runs = store.get_recent_runs(limit=100)
    model_stats = store.get_model_stats()
    project_costs = store.get_project_costs()

    total_runs = len(recent_runs)
    cached_runs = sum(1 for run in recent_runs if run.get("cached"))
    failures = sum(1 for run in recent_runs if not run.get("ok"))
    total_cost = round(sum(float(item.get("total_cost", 0.0) or 0.0) for item in project_costs), 6)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Recent runs", total_runs)
    col2.metric("Cache hits", cached_runs)
    col3.metric("Failures", failures)
    col4.metric("Estimated cost", f"${total_cost:.4f}")

    st.subheader("Recent delegations")
    st.dataframe(recent_runs, use_container_width=True)

    st.subheader("Model success rates")
    st.dataframe(model_stats, use_container_width=True)

    st.subheader("Project cost tracking")
    st.dataframe(project_costs, use_container_width=True)

    st.subheader("Replay a failed run")
    failed_runs = [run for run in recent_runs if not run.get("ok")]
    if failed_runs:
        options = {f"{run['id']} - {run['summary'] or run['error']}": run["id"] for run in failed_runs}
        selected = st.selectbox("Failed run", list(options.keys()))
        payload = store.get_run(options[selected])
        st.json(payload)
    else:
        st.info("No failed runs have been recorded yet.")


def main() -> None:
    render_dashboard()


if __name__ == "__main__":
    main()

