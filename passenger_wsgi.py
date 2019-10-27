import os, sys

# Use Python 3.7.1 interpreter
INTERP = "/home/chriswilson1982/opt/python-3.7.1/bin/python3"
# INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP:
	os.execl(INTERP, INTERP, *sys.argv)

# Add current directory to path, if isn't already 
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import bottle
from bottle import route, run, template

# Define needed routes here	
# See cvmp.py for routes
import cvmp

# Setup Dreamhost passenger hook
def application(environ, start_response):
    return bottle.default_app().wsgi(environ,start_response)	

# Main method for local development	
if __name__ == "__main__":
    bottle.debug(True)
    run()