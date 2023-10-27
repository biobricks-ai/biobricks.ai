####################
Command Line Interface
####################

The biobricks cli has global and local commands. 

Global
======
Commands like configure, version, install that are not specific to a directory. 

When using a command like install, uninstall and assets, you can use a :ref:`brickref` to refer to the asset you want to install.

Run biobricks with no commands for a help message.

.. code-block:: console

  $ biobricks
  Usage: biobricks [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.

  GLOBAL: modify global config and installed bricks:
    configure  configure brick path and token
    install    Install a data dependency
    uninstall  Uninstall a data dependency
    assets     List assets in a data dependency
    version    Get version and check for updates

  LOCAL: build new bricks and manage their dependencies:
    init       Initialize a .bb directory for data dependencies
    add        Import a data dependency
    pull       install local dependencies
    status     Show the status of the local brick

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
Adds a :ref:`brickref` to the dependencies.txt file.

.. code-block:: console

  $ biobricks add <brickref>

pull
******************
Installs all the bricks references in the dependencies.txt.

.. code-block:: console

  $ biobricks pull