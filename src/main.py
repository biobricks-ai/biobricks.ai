import sys
from dvcportal.app import app as dvcportal
from bbportal.app import app as bbportal

if sys.argv[1] == "bbportal":
  bbportal.run('0.0.0.0',5000)

if sys.argv[1] == "dvcportal":
  dvcportal.run('0.0.0.0',5000)