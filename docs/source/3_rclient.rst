==============
R Client
==============

The biobricks R client is nearing completion but is not yet available.

.. Biobricks can be used in R after installation with `pip install biobricks`. 
.. The R client is designed to work along with the biobricks command line tool.

.. Installation
.. ===============
.. The R client can be installed from `github.com/biobricks-ai/biobricks-r <https://github.com/biobricks-ai/biobricks-r>`_ with:

.. .. code-block:: R

..     > remotes::install_github("biobricks/biobricks-r")

.. Install Bricks in R
.. ====================
.. Install bricks using the :ref:`command line client`

.. .. code-block:: console

..     $ biobricks install clinvar # replace clinvar with the desired brick


.. Load Data in R
.. ===============
.. Loading a :ref:`brickref` returns an R list with 
.. all of the objects in the brick. The list has autocompletion for 
.. individual brick assets.

.. Today, most brick assets are Arrow Tables. Soon, some bricks will
.. distribute hdf5 objects for neural networks.

.. .. code-block:: R

..     > library(biobricks)
..     > clinvar <- biobricks::brick_load("clinvar")