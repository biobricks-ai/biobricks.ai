==================
How does it work?
==================

Biobricks.ai is a data-registry that relies on `DVC <https://dvc.org/>`_ to allow users to quickly download versioned data assets. 

When Biobricks is installed and configured a biobricks.ai token and local BBLIB path are chosen. Data assets are stored in the BBLIB with a simple versioning scheme.

Installing Bricks Globally
===========================

Every biobrick is a git repo. When a brick is installed, that git repo
is cloned into the BBLIB. 

Every biobrick is also a dvc repository. When a brick is installed, the
cache of the brick is set to the BBLIB / cache directory. This means that
every data asset stored in a brick has a symlink to the BBLIB / cache 
directory. This helps with data deduplication. 

Loading Bricks
==================

When a brick is loaded in python or R, the respective package 
reviews the brick's path in the BBLIB and creates objects 
based on the cached files in the dvc cache and their paths.

.. TODO update when hdf5 is added

Today, each biobrick can only store parquet files, a 
special file format for tabular data. In the future, more file formats 
will be added to the biobricks system.