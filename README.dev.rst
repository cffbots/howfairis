``howfairis`` developer documentation
=====================================

If you're looking for user documentation, go `here <README.rst>`_.

|
|

Development install
-------------------

.. code:: shell

    # Create a virtualenv, e.g. with
    python3 -m venv venv3

    # activate virtualenv
    source venv3/bin/activate

    # (from the project root directory)
    # install howfairis as an editable package
    pip install --no-cache-dir --editable .
    # install development dependencies
    pip install --no-cache-dir --editable .[dev]

Afterwards check that the install directory was added to the ``PATH``
environment variable. You should then be able to call the executable,
like so:

.. code:: shell

    howfairis https://github.com/<owner>/<repo>

Running the tests
-----------------

Running the tests requires an activated virtualenv with the development tools installed.

.. code:: shell

    # unit tests with mocked representations of repository behavior
    pytest
    pytest tests/
    
    # live tests with actual repository behavior (slow, prone to HttpError too many requests)
    pytest livetests/
    
    # command line interface tests
    bash clitests/script.sh

Running linters locally
-----------------------

Running the linters requires an activated virtualenv with the development tools installed.

.. code:: shell

    # linter
    prospector

    # recursively check import style for the howfairis module only
    isort --recursive --check-only howfairis

    # recursively check import style for the howfairis module only and show
    # any proposed changes as a diff
    isort --recursive --check-only --diff howfairis

    # recursively fix  import style for the howfairis module only
    isort --recursive howfairis

.. code:: shell

    # requires activated virtualenv with development tools
    prospector && isort --recursive --check-only howfairis

You can enable automatic linting with ``prospector`` and ``isort`` on commit like so:

.. code:: shell

    git config --local core.hooksPath .githooks

Versioning
----------

Bumping the version across all files is done with bump2version, e.g.

.. code:: shell

    bump2version minor


Making a release
----------------

Preparation
^^^^^^^^^^^

1. Update the ``CHANGELOG.md``
2. Verify that the information in ``CITATION.cff`` is correct, and that ``.zenodo.json`` contains equivalent data
3. Make sure the version has been updated.
4. Run the unit tests with ``pytest tests/``
5. Run the live tests with ``pytest livetests/``
6. Run the clitests with ``bash clitests/script.sh``

PyPI
^^^^

In a new terminal, without an activated virtual environment or a venv3 directory:

.. code:: shell

    cd $(mktemp -d --tmpdir howfairis.XXXXXX)
    git clone https://github.com/fair-software/howfairis.git .
    python3 -m venv venv3
    source venv3/bin/activate
    pip install --no-cache-dir .
    pip install --no-cache-dir .[publishing]
    rm -rf howfairis.egg-info
    rm -rf dist
    python setup.py sdist bdist_wheel

    # upload to test pypi instance (requires credentials)
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

In a new terminal, without an activated virtual environment or a venv3 directory:

.. code:: shell
    
    cd $(mktemp -d --tmpdir howfairis-test.XXXXXX)

    # check you don't have an existing howfairis
    which howfairis
    python3 -m pip uninstall howfairis

    # install in user space from test pypi instance:
    python3 -m pip -v install --user --no-cache-dir \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple howfairis

Check that the package works as it should when installed from pypitest.

Then upload to pypi.org with:

.. code:: shell

    # Back to the first terminal,
    # FINAL STEP: upload to PyPI (requires credentials)
    twine upload dist/*

GitHub
^^^^^^

Don't forget to also make a release on GitHub.

DockerHub
^^^^^^^^^

To build the image, run:

.. code:: shell

    docker build -t fairsoftware/howfairis:latest .
    
.. code:: shell

    VERSION=<your-version>
    docker tag fairsoftware/howfairis:latest fairsoftware/howfairis:${VERSION}

Check that you have the tags you want with:

.. code:: shell

    docker images

To push the image to DockerHub, run:

.. code:: shell

    # (requires credentials)  
    docker login
    docker push fairsoftware/howfairis:${VERSION}
    docker push fairsoftware/howfairis:latest    
    
The new image and its tags should now be listed here https://hub.docker.com/r/fairsoftware/howfairis/tags?page=1&ordering=last_updated.
    
