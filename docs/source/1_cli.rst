####################
Command Line Client
####################

Installing biobricks adds the biobricks cli to your path. The biobricks 
cli has global and local commands. 

Global
======

configure
**************
Create a .biobricks config file in the home directory. Choose a 
path, BBLIB, to store your bricks, and choose a token from 
`biobricks.ai/token <https://biobricks.ai/token>`_.
Rerun to change the bblib or token.

.. code-block:: console

  $ biobricks configure

install
**************
Install a brick into the brick library. 
:ref:`brickref`


.. code-block:: console

  $ biobricks install <brickref>

After installing a brick it can be used in the :ref:`python client` or :ref:`R client` by running the respective load commands.

Local
=====

Commands for building a new brick with dependencies on other bricks.

init
*****************************
Initializes a new brick repository by creating a .bb directory
in the current directory and adding .bb/dependencies.txt

.. code-block:: console

  $ biobricks init


add
******************
Adds a :ref:`brickref` to the dependencies.txt file and creates a 
symlink to the :ref:`brickref` assets in the .bb directory. 

When brick assets are loaded by the brick, they are loaded from the
.bb directory.

.. code-block:: console

  $ biobricks add <brickref>

pull
******************
Installs all the bricks references in the dependencies.txt.

.. code-block:: console

  $ biobricks pull