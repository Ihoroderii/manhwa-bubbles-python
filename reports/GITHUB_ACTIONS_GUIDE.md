# GitHub Actions Setup Guide

This repository includes several GitHub Actions workflows for automated package management.

## Workflows Included

### 1. Build and Test (`build-and-test.yml`)
- **Triggers**: Push to main, Pull Requests
- **Purpose**: Tests the package on multiple Python versions
- **Actions**: Runs tests, builds package, uploads artifacts

### 2. Publish to PyPI (`publish-to-pypi.yml`)
- **Triggers**: When a GitHub release is published
- **Purpose**: Automatically publishes to PyPI and TestPyPI
- **Requirements**: PyPI trusted publishing setup

### 3. Publish to GitHub (`publish-to-github.yml`)
- **Triggers**: Push to main, tags, releases
- **Purpose**: Creates GitHub package artifacts
- **Actions**: Builds and stores package files

### 4. Create Release (`create-release.yml`)
- **Triggers**: When a git tag starting with 'v' is pushed
- **Purpose**: Automatically creates GitHub releases
- **Actions**: Builds package, generates release notes, uploads assets

## Setup Instructions

### 1. Enable GitHub Actions
Your workflows are already configured! They will run automatically when you push code.

### 2. Setup PyPI Trusted Publishing (for automatic PyPI publishing)

1. **Create PyPI Account**: https://pypi.org/account/register/
2. **Add Trusted Publisher**:
   - Go to: https://pypi.org/manage/account/publishing/
   - Add trusted publisher with:
     - Owner: `ihoroderii`
     - Repository: `manhwa-bubbles`
     - Workflow: `publish-to-pypi.yml`
     - Environment: `pypi`

3. **Create TestPyPI Account**: https://test.pypi.org/account/register/
4. **Add TestPyPI Trusted Publisher**:
   - Go to: https://test.pypi.org/manage/account/publishing/
   - Use same settings but environment: `testpypi`

### 3. Create Your First Release

```bash
# Update version in setup.py and manhwa_bubbles/__init__.py
# Then create and push a tag:
git tag v1.0.1
git push origin v1.0.1
```

This will automatically:
1. Create a GitHub release
2. Build the package
3. Publish to TestPyPI and PyPI (if configured)

## Manual Operations

### Build Package Locally
```bash
python -m build
```

### Test Package
```bash
python test_library.py
```

### Manual PyPI Upload (if not using automation)
```bash
pip install twine
twine upload dist/*
```

## Status Badges

Add these to your README.md:

```markdown
![Build Status](https://github.com/ihoroderii/manhwa-bubbles/workflows/Build%20and%20Test/badge.svg)
![PyPI](https://img.shields.io/pypi/v/manhwa-bubbles)
![Python Version](https://img.shields.io/pypi/pyversions/manhwa-bubbles)
```