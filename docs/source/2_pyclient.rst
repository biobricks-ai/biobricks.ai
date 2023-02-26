==============
Python Client
==============

Biobricks can be used in python after installation with `pip install biobricks`.

The python client is designed to work along with the biobricks command line tool.

Install Bricks
===============
It is recommended to install bricks with the biobricks command line tool.
However, it is possible to install bricks from a python repl with:

.. code-block:: python

    >>> import biobricks as bb
    >>> bb.install("clinvar") # replace 'clinvar' with your brickref


Load Data
===============
loading a :ref:`brickref` returns a python namespace with 
all of the objects in the brick. The namespace has autocompletion for 
individual brick assets.

Today, most brick assets are Arrow Tables. Soon, some bricks will
distribute hdf5 objects for neural networks.

.. code-block:: python

    >>> import biobricks as bb
    >>> clinvar <- bb.load("clinvar")