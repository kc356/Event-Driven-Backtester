"""
Setup script for Event-Driven Backtester.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = [
    "pandas>=1.3.0",
    "numpy>=1.21.0",
    "yfinance>=0.1.70",
    "scikit-learn>=1.0.0",
    "matplotlib>=3.5.0",
    "seaborn>=0.11.0",
    "pytest>=6.0.0",
    "pytest-cov>=2.12.0",
    "mypy>=0.910",
    "black>=21.0.0",
    "flake8>=3.9.0"
]

setup(
    name="event-driven-backtester",
    version="1.0.0",
    author="Event-Driven Backtester Team",
    author_email="team@backtester.com",
    description="A comprehensive event-driven backtesting framework for quantitative trading strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/event-driven-backtester",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "mypy>=0.910",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "backtest=run_backtest:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.json", "*.yaml"],
    },
) 