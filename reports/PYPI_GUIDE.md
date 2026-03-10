# PyPI Publication Guide for manhwa-bubbles

## You now have 3 ways to distribute your pip package:

### Option 1: Direct Installation (Already Working!)
Your package can be installed directly from GitHub:
```bash
pip install git+https://github.com/ihoroderii/manhwa-bubbles.git
```

### Option 2: Local Wheel Distribution
Share the wheel file with others:
```bash
# From the dist/ folder, share: manhwa_bubbles-1.0.0-py3-none-any.whl
# Others can install with:
pip install manhwa_bubbles-1.0.0-py3-none-any.whl
```

### Option 3: Publish to PyPI (Official Python Package Index)

#### Step 3a: Test on TestPyPI First
1. Create account at https://test.pypi.org/
2. Upload to test:
   ```bash
   twine upload --repository testpypi dist/*
   ```
3. Test install from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ manhwa-bubbles
   ```

#### Step 3b: Publish to Real PyPI
1. Create account at https://pypi.org/
2. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```
3. Anyone can install with:
   ```bash
   pip install manhwa-bubbles
   ```

## Important Notes:
- Package name "manhwa-bubbles" must be unique on PyPI
- Once published, you cannot reuse the same version number
- Consider checking if the name is available first at https://pypi.org/project/manhwa-bubbles/

## Your package is ready! 🎉
The files in dist/ folder are your pip-installable packages.