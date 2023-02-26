==============
Build a Brick
==============

Biobricks makes it easier to build data assets that rely on other data 
assets. It does this by treating data assets in a similar way to the 
methods used by package managers.

Initialize
============

When building a new brick first create a new directory and run:

.. code-block:: bash

    $ biobricks init

This creates a .bb subdirectory with a dependencies.txt which will
list the brick dependencies that this asset will rely on. 

The .bb directory also contains symlinks to the data assets stored 
in the :ref:`BBLIB`

Add Brick dependencies
=======================
To add a dependency to a brick, run:

.. code-block:: bash

    $ biobricks add <dependency>

This adds a line to the .bb/dependencies.txt file, installs the dependency
if it is not already installed, and creates a symlink to it in the 
.bb directory.

Working with others
=========================
When working with the same BBLIB as other developers, they can seemlessly
clone and branch your project with confidence that they are using the same
brick dependencies as you. 

If you are working with partners who are using a different BBLIB, 
they can run:

.. code-block:: bash

    $ biobricks pull
  
This command will install all the dependencies listed in .bb/dependencies.txt
and create symlinks to them in the .bb directory.