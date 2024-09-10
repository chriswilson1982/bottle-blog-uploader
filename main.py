import os
import sys
from bottle import Bottle, route, run, template
import blog_uploader # Custom routes

app = Bottle()

if os.getenv('APP_LOCATION') == 'heroku':
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
