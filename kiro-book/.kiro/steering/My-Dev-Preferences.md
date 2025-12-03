---
inclusion: always
---

# Coding Preference

You have a preference for writing code in Python. 

## Python Frameworks

When creating Python code, use the following guidance:

- Use Flask as the web framework
- Follow Flask's application factory pattern
- Use Pydantic for data validation
- Use environment variables for configuration
- Implement Flask-SQLAlchemy for database operations

## Project Structure and Layout

Use the following project structure

```
├ app
	├── src
	├── src/static/
	├── src/models/
	├── src/routes/
	├── src/templates/
	├── src/extensions.py
```

# Python Package Management with uv

Use uv exclusively for Python package management in all projects.

## Project Initialization

Before adding dependencies, always initialize the uv project first:

- Initialize a new Python project: `uv init`
- This creates `pyproject.toml` and sets up the project structure
- Only run `uv init` once per project at the start

## Package Management Commands

- All Python dependencies **must be installed, synchronized, and locked** using uv
- Never use pip, pip-tools, poetry, or conda directly for dependency management

Use these commands:

- Install dependencies: `uv add <package>`
- Remove dependencies: `uv remove <package>`
- Sync dependencies: `uv sync`
- Install from existing pyproject.toml: `uv sync`

## Running Python Code

- Run a Python script with `uv run <script-name>.py`
- Run Python tools like Pytest with `uv run pytest` or `uv run ruff`
- Launch a Python repl with `uv run python`

## Workflow for New Projects

1. First: `uv init` to initialize the project
2. Then: `uv add <packages>` to add dependencies
3. Finally: `uv run <script>.py` to run code