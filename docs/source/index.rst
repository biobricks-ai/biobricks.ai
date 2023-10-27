.. toctree::
   :hidden:
   :maxdepth: 2
   
   self
   1_cli.rst
   4_buildbrick
   5_howwork
   6_reference

=====================================
Quickstart
=====================================

To start using biobricks just:

.. code-block:: console

   $ pip install biobricks   
   $ biobricks configure # select a path for your data and get a token
   $ biobricks install clinvar # or any other database

Installing A Brick
******
clinvar is a database of clinically relevant genetic variants. First, install it:

.. code-block:: console
   
   $ biobricks install clinvar

Each brick distributes a set of assets as filesystem paths (starting at :ref:`BBLIB <bblib>`)

.. code-block:: console

   $ biobricks assets clinvar
   hgvs4variation_parquet: <BBLIB>/brick/hgvs4variation.parquet       
   submission_summary_parquet: <BBLIB>/brick/submission_summary.parquet                                                                                                                                                

Each of the clinvar assets are parquet files, which can be easily accessed
in python and R:

**Python Example**

To use biobricks in python, first install the command line client (see Quickstart). 
The python client is only meant to provide the ``assets`` function, which returns 
a namespace with paths to the assets distributed by a named brickref.

.. code-block:: python

   >>> import biobricks, pandas
   >>> clinvar = biobricks.assets('clinvar')
   >>> pandas.read_parquet(clinvar.allele_gene_parquet)
      AlleleID   GeneID   Symbol                                              Name  GenesPerAlleleID ...  
   0  15041.0    9907.0    AP5Z1  adaptor related protein complex 5 subunit zeta 1               1.0
   1  15042.0    9907.0    AP5Z1  adaptor related protein complex 5 subunit zeta 1               1.0
   ...

**R Example**

To use biobricks in R, first install the command line client (see Quickstart). 
The R client is only meant to provide the ``bbassets`` function, which returns a list 
with paths to the assets distributed by a named brickref.

.. code-block:: R

   > clinvar = biobricks::bbassets('clinvar')
   > arrow::open_dataset(clinvar$allele_gene_parquet) |> head() |> dplyr::collect()
   # A tibble: 6 × 7
   #   AlleleID GeneID Symbol  Name                  GenesPerAlleleID Category Source
   # *    <dbl>  <dbl> <chr>   <chr>                            <dbl> <chr>    <chr> 
   # 1    15041   9907 AP5Z1   adaptor related prot…                1 within … submi…
   # 2    15042   9907 AP5Z1   adaptor related prot…                1 within … submi…


A list of available bricks can be found at 
`status.biobricks.ai <https://status.biobricks.ai>`_.

