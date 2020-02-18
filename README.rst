python-clubhouse-lib |PyPI Version| |PyPI Monthly downloads|
============================================================

The unofficial Python client library for the Clubhouse API.
-----------------------------------------------------------

python-clubhouse-lib is a Python wrapper around the Clubhouse API. It leverages
typed dicts to better provide utility to the programmer when dealing with
Clubhouse data. This library only provides the basic glue between your
application and Clubhouse, and it doesn't attempt to do anything more than that.

Installation
------------

::

    pip install clubhouse-lib

or

::

    git clone https://github.com/huntrar/python-clubhouse-lib
    cd clubhouse_lib
    python setup.py install

Examples
--------

Initializing the client

::

    import clubhouse_lib, os
    cc = clubhouse_lib.ClubhouseClient(os.environ.get('CLUBHOUSE_API_TOKEN'))

Listing Projects

::

    projects = cc.listProjects()

Listing Stories

::

    stories = cc.listStories(projects[0]['id'])

Update Story

::

    cc.updateStory(stories[0]['id'], name='Hello World!')

Contributing
------------

This project contains tooling for easily importing documentation from the
Clubhouse API and converting it into Python.

The API slurper allows you to convert snippets of documentation into JSON
objects, which can then be digested by the API builder which will build the
Python code.

We use Black for code formatting. Our flake8 linting configuration is included
in the repository.

.. |PyPI Version| image:: https://img.shields.io/pypi/v/clubhouse-lib.svg
   :target: https://pypi.python.org/pypi/clubhouse-lib
.. |PyPI Monthly downloads| image:: https://img.shields.io/pypi/dm/clubhouse-lib.svg?style=flat
   :target: https://pypi.python.org/pypi/clubhouse-lib
