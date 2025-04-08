# Contributing to Adaptive RAG

Thank you for your interest in contributing to Adaptive RAG! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/affanrasheed/Adaptive_RAG.git
   cd Adaptive_RAG
   ```

3. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. Create a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Code Style

This project follows PEP 8 style guidelines. We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting

To check your code:
```bash
black --check src tests
isort --check src tests
flake8 src tests
```

To automatically format your code:
```bash
black src tests
isort src tests
```

## Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your changes, following these guidelines:
   - Add appropriate docstrings and type hints
   - Write unit tests for new functionality
   - Update documentation as necessary

3. Test your changes:
   ```bash
   pytest tests/
   ```

4. Commit your changes following [conventional commits](https://www.conventionalcommits.org/) format:
   ```bash
   git commit -m "feat: add new feature"
   ```

## Adding a New UI

If you want to add a new UI implementation:

1. Create a new file in the `ui/` directory (e.g., `ui/my_custom_ui.py`)
2. Implement your UI, following the patterns in existing UIs
3. Update the `ui/launch_ui.py` script to include your new UI option
4. Add documentation and screenshots to the appropriate README files

## Modifying Components

The system is designed to be modular. When modifying components:

1. Maintain backward compatibility when possible
2. Update relevant tests to reflect changes
3. Update docstrings and documentation
4. If you're adding new model types or external services, make them optional

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Run the test suite to make sure all tests pass
3. Push your changes to your fork
4. Submit a pull request to the main repository

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. The maintainers will review your code for:
   - Functionality
   - Code quality
   - Test coverage
   - Documentation
2. Feedback will be provided directly on the pull request
3. Changes may be requested before a pull request is merged

## Questions?

If you have questions about the development process or need help, please open an issue on GitHub.

Thank you for contributing to Adaptive RAG!