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
First, `install git <https://github.com/insilica/srvc-template>`_ and `install dvc <https://dvc.org/doc/install>`_:

.. code-block:: console

   $ apt-get install git
   $ pip install dvc

Then install the python, R, or command line client:  

* python `pypi.org/project/biobricks <https://pypi.org/project/biobricks>`_
* R `github.com/biobricks-ai/biobricks-r <https://github.com/biobricks-ai/biobricks-r>`_
* command line **COMING SOON**


Get a Brick
===========

.. code-block:: console

   $ apt-get install git
   $ pip install dvc
   
Are you new to SRVC? This is the place to start!

* :doc:`Overview <overview>`
* :doc:`Reference <ref/index>`

Quickstart
==========
First, :doc:`Install SRVC <installation>`, then clone `srvc-template <https://github.com/insilica/srvc-template>`_  and :

.. code-block:: console

   $ git clone https://github.com/insilica/sfac.git
   $ cd srvc-template
   $ sr flow pubmed-search # Pull "angry bees" from pubmed
   $ sr flow label # Start labeling interface on port 5005

Now you can alter ``sr.yaml`` to modify the pubmed query or begin building your own SRVC projects.