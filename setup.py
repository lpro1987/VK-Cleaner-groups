#!/usr/bin/env python3
"""
Setup script for VK Cleaner.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vk-cleaner-groups",
    version="1.0.0",
    author="VK Cleaner",
    description="A tool to delete/leave all groups and communities in VKontakte",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lpro1987/VK-Cleaner-groups",
    py_modules=["vk_cleaner", "config"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "vk-cleaner=vk_cleaner:main",
        ],
    },
)