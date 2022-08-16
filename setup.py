import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="kis-api",
    version="0.0.1",
    description="Korea Investment Developers API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duveen/kis-api",
    author="Developer Duveen",
    author_email="duveen@duveen.me",
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Software Development",
        "License :: MIT",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only"
    ],
    license_files=('LICENSE',),
    keywords="kis, rest-api, korea investment",
    packages=find_packages(where="."),
    install_requires=[
        "requests"
    ],
    extras_require={
        "dev": [
            "pytest"
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/duveen/kis-api/issue",
        "Source": "https://github.com/duveen/kis-api"
    }
)
