# Contributing to the MoviePy MCP Video Generation Service

First off, thank you for considering contributing! We love our community and welcome all contributions, from bug reports to new features. This project thrives on the involvement of people like you.

This document provides guidelines for contributing to the project to ensure a smooth and effective process for everyone.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as GitHub Issues. Before creating a bug report, please perform a [search](https://github.com/your-username/moviepy-mcp/issues) to see if the problem has already been reported. If it has and the issue is still open, add a comment to the existing issue instead of opening a new one.

**Bug Report Template**:
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Call endpoint '...' with payload '....'
2. See error message '....'

**Expected behavior**
A clear and concise description of what you expected to happen.

**Logs & Screenshots**
If applicable, add screenshots or log output to help explain your problem.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.12.1]
- Project Version: [e.g., 0.1.0]
```

### Suggesting Features

We love new ideas! To suggest a feature, please create a new issue using the feature request template.

**Feature Request Template**:
```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is. Ex. "I'm always frustrated when..."

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### Submitting Pull Requests

If you're ready to contribute code, the pull request process is the way to go. Please fork the repository, create a new branch, and submit your changes.

---

## Development Setup

#### Prerequisites
-   Python 3.12+
-   [uv](https://github.com/astral-sh/uv) (a fast Python package installer)
-   FFmpeg (see [README.md](README.md) for installation instructions)
-   Git

#### Setup Instructions
```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork locally
git clone https://github.com/<your-username>/moviepy-mcp.git
cd moviepy-mcp

# 3. Install project dependencies and development tools
uv sync --all-extras

# 4. Run the tests to ensure everything is set up correctly
uv run pytest

# 5. Start the development server
uv run uvicorn src.video_gen_service.main:app --reload
```

---

## Development Workflow

#### Branch Naming
Please use a consistent branch naming convention to help us understand the purpose of your changes.
-   `feature/<description>` for new features (e.g., `feature/add-subtitles-effect`)
-   `fix/<description>` for bug fixes (e.g., `fix/resolve-concatenation-error`)
-   `docs/<description>` for documentation changes (e.g., `docs/update-api-examples`)
-   `refactor/<description>` for code refactoring (e.g., `refactor/optimize-resize-function`)
-   `test/<description>` for adding or improving tests (e.g., `test/add-compositing-tests`)

#### Commit Messages
We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps in automating changelogs and makes the project history more readable.

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(api): add endpoint for video watermarking
fix(mcp): correct parameter type for cut_video tool
docs(readme): add docker deployment instructions
```

---

## Coding Standards

#### Style Guide
-   We follow **PEP 8** for all Python code.
-   We use `black` for code formatting and `ruff` for linting (configuration is in `pyproject.toml`).
-   Docstrings should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#3.8-comments-and-docstrings).

#### Best Practices
-   Write clear, self-documenting code.
-   Add comments only for complex or non-obvious logic.
-   Keep functions and classes small and focused on a single responsibility.
-   Add type hints to all function signatures.

---

## Testing

#### Writing Tests
-   New features **must** include corresponding unit tests.
-   Bug fixes **should** include a test case that reproduces the bug and verifies the fix.
-   Tests are located in the `/tests` directory and follow the `test_*.py` naming convention.

#### Running Tests
```bash
# Run all tests
uv run pytest

# Run tests with code coverage report
uv run pytest --cov=src
```

#### Test Coverage
We aim for high test coverage. Please ensure your contributions do not decrease the overall coverage percentage.

---

## Documentation

#### Code Documentation
-   All public functions, classes, and methods must have a docstring.
-   Explain the purpose of the code, its parameters, and what it returns.

#### README Updates
-   If you add a new feature, endpoint, or configuration option, please update the `README.md` accordingly.

---

## Pull Request Process

1.  **Before Submitting**
    -   Ensure all tests pass locally: `uv run pytest`
    -   Update the `README.md` and any other relevant documentation.
    -   Make sure your code is formatted and linted.
    -   Self-review your changes to catch any obvious issues.

2.  **PR Description Template**
    Please use the following template for your pull request description.

    ```markdown
    ## Description
    A brief description of the changes introduced by this PR.

    ## Type of Change
    - [ ] Bug fix (non-breaking change which fixes an issue)
    - [ ] New feature (non-breaking change which adds functionality)
    - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
    - [ ] Documentation update

    ## Related Issues
    Fixes #(issue number)

    ## Testing
    Describe the tests you ran to verify your changes.
    - [ ] All tests pass locally (`uv run pytest`).
    - [ ] Added new tests for my feature/fix.

    ## Checklist
    - [ ] My code follows the style guidelines of this project.
    - [ ] I have performed a self-review of my own code.
    - [ ] I have commented on my code, particularly in hard-to-understand areas.
    - [ ] I have made corresponding changes to the documentation.
    - [ ] My changes generate no new warnings.
    ```

3.  **Review and Merging**
    -   A project maintainer will review your PR.
    -   Please address any feedback or requested changes.
    -   Once approved and all automated checks have passed, your PR will be merged.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
