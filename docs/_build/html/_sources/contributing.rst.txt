Contributing
============

Thank you for your interest in contributing to the Event-Driven Backtester!

Getting Started
--------------

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install in development mode

.. code-block:: bash

   git clone https://github.com/yourusername/event-driven-backtester.git
   cd event-driven-backtester
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"

Development Workflow
-------------------

1. Create a feature branch:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes
3. Run tests and quality checks:

   .. code-block:: bash

      make all

4. Commit your changes with a descriptive message
5. Push to your fork
6. Create a pull request

Code Style
----------

We use several tools to maintain code quality:

* **Black**: Code formatting
* **Flake8**: Linting
* **MyPy**: Static type checking
* **Pre-commit**: Git hooks

Run these tools before committing:

.. code-block:: bash

   make format    # Format code with Black
   make lint      # Run linting checks
   make test      # Run tests

Testing
-------

Write tests for new features:

.. code-block:: bash

   # Run all tests
   python -m pytest tests/ -v

   # Run with coverage
   python -m pytest tests/ -v --cov=src

   # Run specific test
   python -m pytest tests/test_data_handler.py::test_yahoo_data_handler_loads_data -v

Documentation
-------------

Update documentation when adding new features:

1. Update docstrings in your code
2. Add examples to the documentation
3. Update relevant documentation files

Building documentation:

.. code-block:: bash

   make docs

Pull Request Guidelines
----------------------

* Write clear, descriptive commit messages
* Include tests for new functionality
* Update documentation as needed
* Ensure all tests pass
* Follow the existing code style

Issues
------

When reporting issues:

* Use the issue template
* Provide a minimal reproduction example
* Include relevant error messages
* Specify your environment (OS, Python version, etc.)

Contact
-------

* GitHub Issues: For bug reports and feature requests
* GitHub Discussions: For questions and general discussion 