Quickstart Guide
================

This section provides a quickstart guide on how to work with the test.

Working with the test
---------------------

1. **Installation**: 
   Make sure you have the necessary packages installed. You can install the required packages using the `requirements.txt`.
   .. code-block:: console
   
      (.venv) $ pip install -U -r requirements.txt

2. **Running the tests**:
   You can run the tests using pytest:
   .. code-block:: console
   
      (.venv) $ pytest

3. **Generating the Documentation**:
   If you need to regenerate this documentation, navigate to the `docs` directory and run:
   .. code-block:: console
   
      (.venv) $ make html

4. **Viewing the Documentation**:
   After running the `make html` command, open `_build/html/index.html` in your web browser to view the generated documentation.