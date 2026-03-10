from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="manhwa-bubbles",
    version="1.1.0",
    author="Ihor Oderii",
    author_email="ihor.oderii@gmail.com",
    description="A Python library for creating manhwa-style speech bubbles and narration boxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ihoroderii/manhwa-bubbles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Artistic Software",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=8.0.0",
    ],
    extras_require={
        "cairo": ["pycairo>=1.20.0"],
        "yolo": [
            "ultralytics>=8.0.0",
            "opencv-python>=4.8.0",
            "numpy>=1.24.0",
        ],
        "test": ["pytest>=7.0.0"],
    },
    keywords="manhwa, comics, speech bubbles, graphics, PIL, drawing",
    project_urls={
        "Bug Reports": "https://github.com/ihoroderii/manhwa-bubbles/issues",
        "Source": "https://github.com/ihoroderii/manhwa-bubbles",
    },
)