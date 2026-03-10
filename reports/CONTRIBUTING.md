# Contributing to Manhwa Bubbles

Thank you for your interest in contributing to manhwa-bubbles!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/manhwa-bubbles.git
   cd manhwa-bubbles
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install in development mode:
   ```bash
   pip install -e .
   pip install Pillow build pytest
   ```

## Running Tests

```bash
python test_library.py
python examples/demo.py
```

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/new-bubble-type
   ```
2. Make your changes
3. Test your changes
4. Commit and push:
   ```bash
   git add .
   git commit -m "Add new bubble type"
   git push origin feature/new-bubble-type
   ```
5. Create a Pull Request

## Adding New Bubble Types

To add a new bubble type:

1. Add the function to `manhwa_bubbles/speech_bubbles.py`
2. Update the `speech_bubble()` function to handle the new type
3. Add examples to `examples/demo.py`
4. Update the README.md documentation
5. Add tests to `test_library.py`

## Code Style

- Use descriptive function and variable names
- Add docstrings to all functions
- Keep functions focused on a single responsibility
- Follow PEP 8 style guidelines

## Release Process

Releases are automated through GitHub Actions:

1. Update version in `setup.py` and `manhwa_bubbles/__init__.py`
2. Create a git tag: `git tag v1.1.0`
3. Push the tag: `git push origin v1.1.0`
4. GitHub Actions will automatically create a release and publish to PyPI