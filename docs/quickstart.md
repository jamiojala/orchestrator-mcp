# Quickstart

## Install

```bash
pip install "orchestrator-mcp[dashboard]"
```

## Configure

```bash
cp .env.example .env
cp orchestrator-mcp.yaml.example orchestrator-mcp.yaml
```

Fill in only the providers you plan to use.

## Validate

```bash
orchestrator-mcp doctor
```

## Run

```bash
orchestrator-mcp serve
```

Optional dashboard:

```bash
orchestrator-mcp dashboard
```
