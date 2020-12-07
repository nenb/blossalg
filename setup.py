import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="blossalg",
    version="1.0.0",
    description="Construct a maximum matching on a graph with the blossom algorithm",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nenb/blossalg",
    author="Nick Byrne",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
    ],
    packages=["blossom"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["blossalg=blossom.__main__:main"]},
)
