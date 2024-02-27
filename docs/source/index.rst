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

   $ pipx install biobricks
   $ biobricks configure # set a path and token
   $ biobricks install clinvar # or any other database

Installing A Brick
********************
clinvar is a database of clinically relevant genetic variants. First, install it:

.. code-block:: console
   
   $ biobricks install clinvar

Each brick has a list of filesystem paths (starting at :ref:`BBLIB <bblib>`)

.. code-block:: console

   $ biobricks assets clinvar
   hgvs4variation_parquet: <BBLIB>/brick/hgvs4variation.parquet       
   submission_summary_parquet: <BBLIB>/brick/submission_summary.parquet                                                                                                                                                

The clinvar assets are parquet files, which can be used in python and R:

**Python Example**

To use biobricks in python, first install the command line client (see Quickstart). 
The ``assets`` function returns a namespace with brick asset paths. 
This also works well with spark, but pandas and pyarrow work well too.

.. code-block:: python

   >>> import biobricks, pandas
   >>> clinvar = biobricks.assets('clinvar') # a namespace with paths to assets
   >>> pandas.read_parquet(clinvar.allele_gene_parquet) 
      AlleleID   GeneID   Symbol                                              Name  GenesPerAlleleID ...  
   0  15041.0    9907.0    AP5Z1  adaptor related protein complex 5 subunit zeta 1               1.0
   1  15042.0    9907.0    AP5Z1  adaptor related protein complex 5 subunit zeta 1               1.0
   ...

**R Example**

To use biobricks in R, first install the command line client (see Quickstart), then install 
the R package from github (see below). The ``bbassets`` function is the main function and it
returns a named list of assets for a given :ref:`brickref <brickref>`.

.. code-block:: R

   > install.packages('biobricks')
   > clinvar <- biobricks::bbassets('clinvar')                   # a named list of assets
   > arrowds <- arrow::open_dataset(clinvar$allele_gene_parquet) # arrow loads parquet files
   > arrowds |> head() |> dplyr::collect()
   # A tibble: 6 × 7
   #   AlleleID GeneID Symbol  Name                  GenesPerAlleleID Category Source
   # *    <dbl>  <dbl> <chr>   <chr>                            <dbl> <chr>    <chr> 
   # 1    15041   9907 AP5Z1   adaptor related prot…                1 within … submi…
   # 2    15042   9907 AP5Z1   adaptor related prot…                1 within … submi…


A list of available bricks can be found at 
`status.biobricks.ai <https://status.biobricks.ai>`_.

