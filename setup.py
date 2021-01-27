import os.path
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

if __name__ == "__main__":
    setup(
        name="blossalg",
        version="1.1.0",
        description=(
            "Construct a maximum matching on a graph with the blossom"
            " algorithm"
        ),
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/nenb/blossalg",
        author="Nick Byrne",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.8",
        ],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        install_requires=["future"],
        extras_requires={
            "tests": ["coverage", "pytest"],
            "dev": ["coverage", "pytest", "pre-commit"],
        },
        entry_points={"console_scripts": ["blossalg=blossom.__main__:main"]},
    )
