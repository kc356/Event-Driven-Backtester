Installation
============

Requirements
------------

* Python 3.8 or higher
* pip (Python package installer)

Dependencies
------------

The Event-Driven Backtester requires the following Python packages:

* pandas >= 1.3.0
* numpy >= 1.21.0
* yfinance >= 0.1.70
* scikit-learn >= 1.0.0
* matplotlib >= 3.5.0
* seaborn >= 0.11.0

Installation Methods
--------------------

From Source
~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/event-driven-backtester.git
      cd event-driven-backtester

2. Create a virtual environment (recommended):

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the package:

   .. code-block:: bash

      # Install in development mode
      pip install -e .

      # Install with development dependencies
      pip install -e ".[dev]"

Using pip
~~~~~~~~~

.. code-block:: bash

   pip install event-driven-backtester

Development Setup
-----------------

For development, install with additional dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

This includes:

* pytest - Testing framework
* pytest-cov - Coverage reporting
* mypy - Static type checking
* black - Code formatting
* flake8 - Linting
* pre-commit - Git hooks

Verification
------------

To verify the installation, run:

.. code-block:: bash

   python -c "from src import Backtest; print('Installation successful!')"

Or run the tests:

.. code-block:: bash

   python -m pytest tests/ -v 