"""Scoresheet install script"""
from setuptools import setup

setup(
    name="scoresheet",
    version="1.1",
    description="Create printable PDF scoresheet for kyykkä competition.",
    py_modules=["scoresheet"],
    entry_points={
        "console_scripts": ["scoresheet=scoresheet:main"]
    },
    install_requires=['PyPDF2', 'appy', 'argcomplete', 'charset-normalizer']
)
