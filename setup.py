from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name="fmpy",
    version="0.1",
    install_requires=required,
    packages=find_packages(),
    include_package_data=False,
)