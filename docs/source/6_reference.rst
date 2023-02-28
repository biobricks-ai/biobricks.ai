:orphan: references

=============
Reference
=============


brickref
=========
Brickrefs are used to reference a brick for 
installation, removal, and loading. Currently,
brickrefs can either be an alphanumeric name eg. "tox21", 
or they can be a git remote with commit eg.
"https://github.com/biobricks-ai/clinvar#f73d05c06a8f662defa143821c2bb15bc4001237".

Future refs may allow references to branches, tags, and releases.

BBLIB
==========
The BBLIB is set for a user by running :code:`biobricks configure`. It is 
a path to a filesystem for storing data assets. It is a good idea to choose a path that has a lot of free space and fast
read times. A mounted SSD is a good choice. 

TOKEN
==========
Biobricks.ai provides a temporary token for testing on install. To receive a permanent token register on biobricks.ai and go to `https://biobricks.ai/token/` to generate a token. Biobricks uses this token to track brick usage, provide support, and generate usage based billing.