import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dart-sass",
    version="0.5.0",
    author="dumdoo",
    description="A wrapper around Dart Sass (https://sass-lang.com/dart-sass)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dumdoo/Py-Dart-Sass",
    project_urls={
        "Bug Tracker": "https://github.com/dumdoo/Py-Dart-Sass/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"dartsass": ["sass/*/*/*", "sass/*/*/src/*"]},
    python_requires=">=3.10",
)
