<img src="/assets/logo.png?width=100" alt="CRSet Logo" width="120" height="120" />

# CRSet

[![License](https://img.shields.io/github/license/uesleibros/crset?style=flat-square)](LICENSE)
[![Last Updated](https://img.shields.io/badge/data-updated%20daily-brightgreen?style=flat-square)](#)
[![Made with Python](https://img.shields.io/badge/made%20with-python-blue?style=flat-square&logo=python)](#)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square&logo=pytest)](#)
[![Coverage](https://img.shields.io/badge/coverage-95%25-success?style=flat-square)](#)
[![OpenAPI](https://img.shields.io/badge/docs-openapi-6BA539?style=flat-square&logo=openapiinitiative)](#)
[![Contributions](https://img.shields.io/badge/contributions-welcome-orange?style=flat-square)](https://github.com/uesleibros/crset/issues)

**CRSet** is a high-performance, developer-focused football API built on top of real-time web scraping from [SoFIFA.com](https://sofifa.com).  
It exposes structured, searchable football data through fast and predictable RESTful endpoints.

## Overview

CRSet transforms raw HTML from SoFIFA into an accessible JSON-based API. It delivers real-time football data for applications, dashboards, data analysis, scouting tools, or anything you want to build on top of player and team information.

- Player and club data with full attributes
- Powerful search and filter queries
- Real-time scraping + smart caching
- Clean, RESTful architecture
- Built with Python and FastAPI


| Component       | Technology         |
|----------------|--------------------|
| Language        | Python 3.11+       |
| Web Framework   | FastAPI            |
| HTTP Server     | Uvicorn (ASGI)     |
| Testing         | Pytest             |
| Documentation   | OpenAPI / Swagger  |
| Data Source     | [SoFIFA](https://sofifa.com) (scraped) |

## Use Cases

- Data ingestion for sports analytics platforms
- Scouting and player comparison tools
- Visualization dashboards
- Academic and statistical research
- Backend services for fantasy football applications

## Legal Notice

This project is **not affiliated with or endorsed** by SoFIFA, EA Sports, FIFA, or any related entity.
All data is scraped from **publicly available** sources and is intended for **educational and non-commercial** use only.

## Contributing

Whether you're fixing bugs, adding features, improving documentation, or enhancing tests, your input is valuable and appreciated.

Before contributing, please read and follow the guidelines below to ensure a smooth and consistent development workflow.

### How to Contribute

1. **Fork the repository**

Create your own fork via GitHub and clone it to your local machine.

2. **Create a feature branch**

Use a descriptive name for your branch:

```sh
git checkout -b feature/player-filter-by-age
```

3. **Write clear, maintainable code**

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style.
- Use type annotations where applicable.
- Maintain consistent naming and structure.
- Add or update docstrings for public methods and modules.

4. **Add tests for new behavior**

- All new features or bug fixes must include unit or integration tests.
- Use `pytest` and ensure 95%+ test coverage is maintained.
- Run the test suite locally before submitting:
  
```sh
pytest --cov=crset
```

5. **Run static analysis and lint checks**

Make sure your code passes linters and formatters:

```sh
black . && isort . && flake8 .
```

6. **Document your changes**

- Update the OpenAPI schema if necessary.
- If your feature introduces a new endpoint, describe it briefly in the README or documentation.

7. **Commit following conventional commit standards**

Examples:

- `feat(api): add position-based filtering`
- `fix(scraper): handle missing club IDs`
- `test: increase coverage for club endpoints`

8. **Push and open a pull request**

- Describe the purpose of the change clearly.
- Reference related issues (e.g., Closes #42).
- Ensure the CI pipeline passes.

## Issue Reporting

When reporting a bug or requesting a feature, please include:

- A clear and descriptive title
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Relevant logs or traceback, if applicable
- Version information (Python version, OS, etc.)

Please check existing issues before opening a new one to avoid duplicates.
