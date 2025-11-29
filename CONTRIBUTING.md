# Contributing to AHTSE

Thank you for your interest in contributing to the AI Hallucination Firewall + Trust Score Engine (AHTSE)! We welcome contributions from the community to help make AI safer and more reliable.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/AHTSE.git
    cd AHTSE
    ```
3.  **Set up the environment**:
    ```bash
    make install
    ```

## Development Workflow

1.  Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature/my-new-feature
    ```
2.  Make your changes. Ensure code quality by running:
    ```bash
    make lint
    make format
    ```
3.  Run tests to ensure no regressions:
    ```bash
    make test
    ```
4.  Commit your changes with clear messages.

## Pull Request Process

1.  Push your branch to GitHub.
2.  Open a Pull Request (PR) against the `main` branch.
3.  Describe your changes clearly in the PR description.
4.  Wait for review and address any feedback.

## Code Style

*   We use **Black** for formatting.
*   We use **Flake8** for linting.
*   We use **MyPy** for static type checking.
*   All new code must include type hints and docstrings.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with details about the problem or suggestion.
