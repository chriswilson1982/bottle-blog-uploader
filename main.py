import os
from bottle import Bottle, run
import blog_uploader

app = Bottle()

if os.environ.get('APP_LOCATION') == 'heroku':
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
