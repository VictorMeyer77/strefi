import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="strefi",
    version=read("strefi", "VERSION"),
    description="Stream each new rows of a file and write in kafka",
    url="https://github.com/VictorMeyer77/strefi",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Victor Meyer",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["strefi = strefi.__main__:main"]},
    extras_require={"test": read_requirements("requirements-test.txt")},
    license_files="LICENSE",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
    ],
    project_urls=(
        {
            "Bug Tracker": "https://github.com/VictorMeyer77/strefi/issues",
            "Changelog": "https://github.com/VictorMeyer77/strefi/blob/main/CHANGELOG.md",
            "Documentation": "https://strefi.readthedocs.io",
            "Source": "https://github.com/VictorMeyer77/strefi",
        }
    ),
)
