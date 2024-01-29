from setuptools import setup, find_packages

version = "0.0.1"
description = "Build local"
with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="quantdb",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="M. Xue",
    author_email="",
    license="Apache",
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    platforms=["Windows", "Linux"],
    keywords="quant, fintech",
    packages=find_packages(),
    install_requires=[
        "pytz",
        "pydantic==1.10.0",
        "akshare==1.9.25",
        "matplotlib==3.2.2",
        "numpy==1.23.4",
        "pandas",
        "pymongo",
    ],
    entry_points={
        'console_scripts': [
            'quantdb=akshare_db.main:main', # run cli
        ],
    },
)
