from setuptools import setup
from setuptools import find_packages

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)