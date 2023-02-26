.. toctree::
   :hidden:
   :maxdepth: 2
   
   self
   1_cli.rst
   2_pyclient
   3_rclient
   4_buildbrick
   5_howwork
   6_reference

=====================================
Quickstart
=====================================

Download public databases in a single line of code. No more learning new APIs, finding download buttons, or building complex ETL pipelines.

Install with pip and then configure with the command line tool:

.. code-block:: console

   $ pip install biobricks   
   $ biobricks configure # complete the prompts
   $ biobricks install clinvar # or any other database

:code:`biobricks configure` creates a :code:`.biobricks` config file in the home directory with a field for:

   1. :code:`BBLIB` the path to install bricks
   2. :code:`TOKEN` authenticates biobricks.ai requests.

Skip the token prompt during configuration for a temporary token. For a 
permanent token, register at `biobricks.ai <https://biobricks.ai>`_ 
and go to `biobricks.ai/token <https://biobricks.ai/token>`_.

After installing a brick it can be used in the :ref:`python client` or :ref:`R client` by running the respective load commands. In python:

.. code-block:: python

   >>> import biobricks, pandas
   >>> clinvar = biobricks.load('clinvar')
   >>> clinvar.var_citations.to_pandas()
      AlleleID  VariationID rs           nsv    citation_source citation_id
   0  15041.0          2.0  397704705.0  None   PubMed          25741868
   1  15041.0          2.0  397704705.0  None   PubMedCentral   4544753
   ...

Loading the brick returns a namespace that can be autocompleted with names for all of the available assets in the installed brick. Data assets are typically parquet Tables (see the `pyarrow <https://arrow.apache.org/docs/python/index.html>`_ and `R arrow <https://arrow.apache.org/docs/r/>`_ packages). 

A list of available bricks can be found at 
`github.com/biobricks-ai <https://github.com/biobricks-ai>`_.

