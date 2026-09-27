from setuptools import setup

# Metadata is declared in pyproject.toml ([project] and [tool.setuptools]),
# which is the canonical source of truth. This shim exists only so legacy
# `setup.py`-driven tooling keeps working.
setup()
