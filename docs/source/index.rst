.. dataprobe documentation master file, created by
   sphinx-quickstart on Mon Jan 28 14:13:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DataProbe: Tests for Data
=========================

.. image:: https://travis-ci.org/nrgoncalves/dataprobe.svg?branch=master
    :target: https://travis-ci.org/nrgoncalves/dataprobe

DataProbe is a simple library for testing your data.

Here is a quick demo. Let's generate some data: ::

  import pandas as pd  
  df = pd.DataFrame(data={'author': ['L. Tolstoy', 'M. Cervantes',
                                     'L. Tolstoy', 'F. Dostoyevsky',
                                     'C. Brontë ', 'J. Austen'],
                          'book': ['Anna Karenina',
			           'Don Quixote',
                                   'War and Peace',
				   'The Brothers Karamazov',
                                   'Jane Eyre',
				   'Emma'],
                          'n_pages': [864, 1605, 1225, 840, 507, 544]})

We have a dataset of great books. For each book, we have a corresponding author and number of pages.
I would like to ensure that a book can only have a single author, but an author can be associated with multiple books.
Also, it doesn't make sense to have a negative number of pages, so I also want to ensure that is not present in the data: ::
  
  import dataprobe as dp
  from dataprobe.correspondence import OneToMany
  from dataprobe.values import Bounded

  probe = dp.DataProbe()
  probe.constrain(Bounded('n_pages', lower=0))
  probe.constrain(OneToMany(['author', 'book']))
  probe.summary

The `summary` method displays a table containing all the constraints I have imposed so far. Now let's see if these are met: ::

  test = probe.run(df)
  test.summary

Now the test has found some violations, so let's see what the problem was: ::

  test.details


API documentation  
=================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dataprobe


Contributing
============

We are using `pytest` for unit tests::

  python -m pytest --cov=dataprobe tests/

and we encourage type annotations and checking via `mypy`, e.g.::

  mypy helpers.py

To update and generate documentation, we use `sphinx`::

  sphinx-build -b html source build


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
