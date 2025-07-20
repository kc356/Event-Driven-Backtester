# Event-Driven Backtester - Project Structure

## Overview

This document describes the improved project structure for the Event-Driven Backtester, which follows Python best practices and modern development standards.

## Directory Structure

```
Event-Driven-Backtester/
├── src/                          # Main source code
│   ├── __init__.py              # Package initialization
│   ├── Main.py                  # Legacy entry point
│   ├── DataHandler.py           # Data handling components
│   ├── Events.py                # Event classes
│   ├── Strategy.py              # Base strategy class
│   ├── Portfolio.py             # Portfolio management
│   ├── Execution.py             # Order execution
│   ├── Performance.py           # Performance metrics
│   ├── PlotPerformance.py       # Performance plotting
│   ├── RiskManagement.py        # Risk management
│   ├── BacktesterLoop.py        # Main backtest engine
│   └── Strategies/              # Trading strategies
│       ├── __init__.py          # Strategy package
│       ├── Buy_And_Hold_Strat.py
│       ├── MAC_Strat.py
│       ├── ETF_Forecast.py
│       ├── OLS_MR_Strategy.py
│       └── Helper/              # Strategy utilities
│           ├── __init__.py
│           └── CreateLaggedSeries.py
├── config/                      # Configuration management
│   ├── __init__.py
│   └── backtest_config.py       # Backtest configuration
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_data_handler.py     # Data handler tests
├── examples/                    # Example scripts
│   ├── __init__.py
│   ├── basic_backtest.py        # Basic backtest example
│   └── strategy_comparison.py   # Strategy comparison
├── docs/                        # Documentation
│   └── README.md               # Documentation guide
├── DataDir/                     # Data storage
├── venv/                        # Virtual environment
├── run_backtest.py             # New entry point
├── setup.py                    # Package setup
├── pyproject.toml              # Modern Python packaging
├── requirements.txt            # Dependencies
├── Makefile                    # Development tasks
├── .pre-commit-config.yaml     # Code quality hooks
├── .gitignore                  # Git ignore rules
├── README.md                   # Project README
├── CONTRIBUTING.md             # Contribution guidelines
└── PROJECT_STRUCTURE.md        # This file
```

## Key Improvements

### 1. **Proper Python Package Structure**
- Added `__init__.py` files for all packages
- Organized imports and exports
- Proper package hierarchy

### 2. **Configuration Management**
- Centralized configuration in `config/backtest_config.py`
- Dataclass-based configuration with type hints
- Default configurations and strategy-specific settings

### 3. **Modern Entry Point**
- New `run_backtest.py` with command-line interface
- Support for multiple strategies and symbols
- Flexible configuration options

### 4. **Development Tools**
- **Makefile**: Common development tasks
- **pre-commit**: Code quality hooks
- **pyproject.toml**: Modern Python packaging
- **setup.py**: Package installation
- **requirements.txt**: Dependency management

### 5. **Testing Infrastructure**
- Moved tests to `tests/` directory
- Proper test organization
- Coverage reporting setup

### 6. **Documentation Structure**
- Organized documentation in `docs/`
- Example scripts in `examples/`
- Clear project documentation

### 7. **Code Quality**
- Type hints throughout the codebase
- Black formatting configuration
- MyPy static type checking
- Flake8 linting

## Usage

### Running Backtests

```bash
# Using the new entry point
python run_backtest.py --symbol TQQQ --start-date 2016-01-01 --end-date 2021-01-01 --strategy ETF_Forecast

# Using the legacy entry point
cd src && python Main.py
```

### Development Commands

```bash
# Install in development mode
make install-dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Run all quality checks
make all

# Clean up
make clean
```

### Example Scripts

```bash
# Run basic example
python examples/basic_backtest.py

# Run strategy comparison
python examples/strategy_comparison.py
```

## Benefits of the New Structure

1. **Maintainability**: Clear separation of concerns and organized code
2. **Scalability**: Easy to add new strategies, data sources, and features
3. **Testing**: Proper test infrastructure with coverage reporting
4. **Documentation**: Comprehensive documentation and examples
5. **Code Quality**: Automated formatting, linting, and type checking
6. **Deployment**: Proper packaging for distribution
7. **Development Experience**: Modern development tools and workflows

## Migration Guide

### For Existing Users
- The old `src/Main.py` still works
- New entry point provides more flexibility
- Configuration can be managed through command-line arguments

### For Developers
- Use the new package structure for imports
- Follow the established patterns for adding new strategies
- Use the development tools for code quality

## Future Enhancements

1. **Web Interface**: Add a web-based backtest interface
2. **Database Integration**: Support for storing results in databases
3. **Real-time Trading**: Live trading capabilities
4. **Advanced Risk Management**: More sophisticated risk controls
5. **Strategy Optimization**: Automated strategy parameter optimization
6. **Performance Analytics**: Enhanced performance metrics and visualization 