import sys
import dvcportal.app
import bbportal.app

if sys.argv[1] == "bbportal":
  app = bbportal.app.create_app()
  app.run('0.0.0.0',5002,debug=True)

if sys.argv[1] == "dvcportal":
  app = dvcportal.app.create_app()
  app.run('0.0.0.0',5001)