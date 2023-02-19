.. BioBricks documentation master file, created by
   sphinx-quickstart on Fri Feb 17 09:58:24 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
=====================================
Get Started
=====================================

SRVC is an open-source document review system that provides full privacy and control over your data.
It is versatile, and can be extended with Python, R, or any other language.
The data model is flexible, and supports managing data with `git <https://git-scm.com/>`_.

.. _index-first-steps:

Install
===========
First, `install git <https://github.com/insilica/srvc-template>`_ then :

.. code-block:: console

   $ pip install biobricks

BioBricks also has an R package `github.com/biobricks-ai/biobricks-r <https://github.com/biobricks-ai/biobricks-r>`_.

Setup
===========
BioBricks works by requesting data with a token from dvc.biobricks.ai and storing it in a local directory:

1. Get your token at biobricks.ai


Quickstart
==========
First, :doc:`Install SRVC <installation>`, then clone `srvc-template <https://github.com/insilica/srvc-template>`_  and :

.. code-block:: console

   $ git clone https://github.com/insilica/sfac.git
   $ cd srvc-template
   $ sr flow pubmed-search # Pull "angry bees" from pubmed
   $ sr flow label # Start labeling interface on port 5005

Now you can alter ``sr.yaml`` to modify the pubmed query or begin building your own SRVC projects.