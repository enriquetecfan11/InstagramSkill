# Contributing

## Local setup

1. Create a virtual environment with Python 3.10 or newer.
2. Install dependencies with `python3 -m pip install -r requirements.txt`.
3. Run `python3 tools/scripts/validate_repo.py` before committing.

## What belongs in Git

Commit the source of the skill, examples, base avatar assets, and scripts:

- `skill/`
- `tools/`
- `examples/`
- `assets/`
- `README.md`
- project configuration files

Do not commit generated carousels, browser diagnostics, local analysis, caches, or scratch exports.
Those folders are intentionally ignored.

## Skill changes

Keep `skill/ig-tech-avatar-posts/SKILL.md` focused on the workflow. Put detailed systems,
templates, prompt blocks, and examples in `skill/ig-tech-avatar-posts/references/`.

When changing rendering behavior, update at least one JSON example if the contract changes.
