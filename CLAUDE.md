# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a DSPy tutorial project for building AI agents. For detailed information about the agent architecture and capabilities, see [AGENTS.md](AGENTS.md).

## Running the Project

```bash
# Run the agent demo
python src/agent.py

# Run the basic main entry point
python main.py
```

## Dependencies

Uses uv for dependency management with Python >=3.13. Key dependencies include DSPy, MLflow, Pydantic, Rich, and python-dotenv.

## Configuration

Environment variables should be configured in `.env` file for OpenAI API access.