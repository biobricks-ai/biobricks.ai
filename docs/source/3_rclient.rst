==============
R Client
==============

The R client is a `reticulate <https://rstudio.github.io/reticulate/>`_ wrapper around the python client. To get started, first install and configure biobricks:

Installation
============
.. code-block:: console
  
  $ pip install biobricks
  $ biobricks configure

Then install the R client:

.. code-block:: R
  
  > library(remotes)
  > install_github("biobricks-ai/biobricks-r",dep=TRUE)
  > biobricks::bblib() # check biobricks library path

The R client has a dependency on :code:`arrow` which is necessary for loading parquet files. This is why the :code:`dep=True` is set in the :code:`install_github` command. If you already have arrow installed, the dep argument can be removed.

On the first usage, the Biobricks R package asks to install miniconda, it uses miniconda to install a copy of the python biobricks package. The biobricks-r functions use the :code:`reticulate` package to call the python biobricks functions.

Loading Bricks
==============
To install and start using a brick use :code:`bbinstall` and :code:`bbload`. The clinvar brick distributes parquet files. This means the arrow package is required to load the brick. 

.. code-block:: R
  
  > biobricks::bbinstall("clinvar") # install the clinvar brick
  > cv <- biobricks::bbload("clinvar")
  > cv$variant_summary |> head() |> dplyr::collect()
  # A tibble: 6 x 34
  #   AlleleID Type     Name  GeneID GeneS~1 HGNC_ID ...
  # *    <dbl> <chr>    <chr>  <dbl> <chr>   <chr>   ...
  # 1    15041 Indel    NM_0~   9907 AP5Z1   HGNC:2~ ...
  # 2    15041 Indel    NM_0~   9907 AP5Z1   HGNC:2~ ...
  # ... 

The R arrow package and biobricks work really well together, arrow can be used to make analysis of biobricks tables much more efficient, all without pulling data into the R session. Learn more about arrow in R here: https://arrow.apache.org/docs/r/articles/arrow.html
