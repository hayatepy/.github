# Contributing to hayatepy

Thank you for helping improve the hayate ecosystem.

## Before opening a pull request

- Use the affected repository's issue tracker for a reproducible bug or a
  focused feature proposal.
- For a public API change, describe the real use case and the standard or
  runtime behavior that motivates it.
- Keep package boundaries intact: the core stays small, and external resources
  are injected through protocols.
- Do not report security vulnerabilities in public issues. Follow
  [SECURITY.md](SECURITY.md).

## Development workflow

Every package uses `uv`, `pytest`, and `ruff`:

```sh
uv sync
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest -q
```

Some repositories add acceptance tests or runtime-specific jobs. Run the
commands documented in that repository before submitting.

## Design partners

If you are evaluating Hayate in an owner-external application and want bounded
onboarding help, read the
[design-partner program](docs/DESIGN_PARTNERS.md). Use its public intake form
instead of filing a speculative framework feature request.

## Pull requests

- Keep a pull request focused on one problem.
- Add tests for behavior changes and update public documentation with the code.
- Explain user impact, compatibility implications, and the checks you ran.
- Pin third-party GitHub Actions by full commit SHA.
- Use English for public documentation, code comments, and API names. Internal
  design notes may use Japanese where the repository already follows that
  convention.

All contributions are accepted under the license of the repository they modify.
