# coding=utf-8

from bottle import Bottle, route, get, post, template, static_file, request
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pytz
import hashlib
import re
from PIL import Image
import io
import paramiko

# Authentication details
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
FTP_HOST = os.environ.get("FTP_HOST")
FTP_REMOTE_PATH = os.environ.get("FTP_REMOTE_PATH")
FTP_USERNAME = os.environ.get("FTP_USERNAME")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD")
BASE_IMAGE_PATH = os.environ.get("BASE_IMAGE_PATH")

# Upload image size for processing
IMAGE_SIZE = (700, 400)

# Some convenience tuple constants
types = ("news", "health")
pub = ("unpublished", "published")

# Store article titles to check for duplicates
titles=[]

# Paramiko setup
paramiko.util.log_to_file("paramiko.log")

# Create Bottle app
app = Bottle()

# STATIC ROUTES

# JavaScript
@app.get('/js/<filename>')
def js_static(filename):
	return static_file(filename, root='./static/js/')

# Images
@app.get('/img/<filename>')
def img_static(filename):
	return static_file(filename, root='static/img/')

# CSS
@app.get('/css/<filename>')
def css_static(filename):
	return static_file(filename, root='./static/css/')

# DYNAMIC ROUTES

# INDEX
@app.get('/')
def index():
	return template("main")

# UPDATE
@app.post('/update')
def update():

	# Get date
	belfast = pytz.timezone('Europe/Belfast')
	now = datetime.now(belfast)
	date = now.strftime('%Y-%m-%d %H:%M:%S')

	# Type
	type_value = request.forms.get("type")
	type = types[int(type_value)]

	# Other parameters
	title = request.forms.get("title").strip()
	body = request.forms.get("body").strip()
	body = parse_to_html(body)
	image = request.forms.get("image")
	author = request.forms.get("author")
	publish_value = request.forms.get("publish")
	publish = 1 if publish_value else 0
	password = request.forms.get("password")
	
	# Check for duplicate titles
	if title in titles:
		return {"result" : 0, "message": "Duplicate Title"}

	# Password check (for file upload - MySQL login requires password separately.)
	hash = hashlib.md5(password.encode()).hexdigest()
	comparator = hashlib.md5(MYSQL_PASSWORD.encode()).hexdigest()
	if hash != comparator:
		# Exit early as password wrong
		return {"result" : 0, "message": "Password Error"}

	# Image upload (optional)
	file = request.files.get("file")

	# FIXME: This uploaded image to folders on Dreamhost, but now running in different domain
	# Python FTP module might work
	# For now, no images (or they can be uploaded manually on Dreamhost)
	
	if file:
		# Get file extension
		extension = file.filename.split(".")[-1]
		if extension.lower() not in ('png', 'jpg', 'jpeg'):
			return {"result" : 0, "message": "File Format Error"}
		
		# Save image file to BytesIO object
		s = io.BytesIO()
		file.save(s)
		# Process image with PIL and save
		im = Image.open(s)
		im = process_image(im, IMAGE_SIZE)
		# Save modified image back to BytesIO object
		t = io.BytesIO()
		im.save(t, format=extension)
		t.seek(0)

		# SFTP setup
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		# Set remote path for storage
		remote_path = FTP_REMOTE_PATH + BASE_IMAGE_PATH + f"/{type}_images/" + file.filename
		
		try:
        		# Connect to the FTP server
			ssh.connect(FTP_HOST, port=22, username=FTP_USERNAME, password=FTP_PASSWORD)
			# Open an SFTP session
			with ssh.open_sftp() as sftp:
				# Use SFTP's putfo to upload the image_data (BytesIO object) to the server
				sftp.putfo(t, remote_path)
				print("Image uploaded successfully!")
		except Error as e:
			print(e)
		finally:
			# Close the SSH connection
			ssh.close()
		
	record = (date, title, body, author, image, publish)
	return mysql_insert(type, record)

# Get previous articles in HTML format
@app.get('/previous')
def get_previous_articles():
	# Connect to MySQL database
	connection, cursor = mysql_connect(False)
	try:
		# connection, cursor = mysql_connect(False)
		cursor.execute("select * from news order by issue desc;")
		news_records = cursor.fetchall()
		cursor.execute("select * from health order by issue desc;")
		health_records = cursor.fetchall()
	except Exception as e:
		print(e)
	finally:
		# Closing database connection
		if(connection.is_connected()):
			cursor.close()
			connection.close()
	
	# Set list of titles to avoid duplicate submission
	global titles
	titles = []
	for item in news_records:
		titles.append(item[2])
	for item in health_records:
		titles.append(item[2])
	
	# Get published counts
	news_publish_count = len([item for item in news_records if item[6] == 1])
	health_publish_count = len([item for item in health_records if item[6] == 1])
	
	# Set strings of HTML to return
	output_string = f"<h1>Previous Articles</h1><h2 class='mt-4'>News</h2><p class='mb-3'>{news_publish_count} of {len(news_records)} articles published</p>"

	middle_string = f"<h2 class='mt-4'>Health Blog</h2><p class='mb-3'>{health_publish_count} of {len(health_records)} articles published</p>"

	for item in news_records:
		border_class = "border-success" if item[6] else "border-danger"
		date_string = f"{item[1].day} {item[1]:%b} {item[1]:%Y}"
		text_class = "text-success" if item[6] else "text-danger"
		text = pub[item[6]].capitalize()

		news_item_string = f"<div class='card w-100 rounded my-3 px-3 py-2 text-dark {border_class}'><p class='card-text'>{item[2]}<br /><small class='text-muted'>{date_string}</small><a class='no-underline float-right {text_class}' href='#!' onclick='changePublish(1, {item[0]}, {item[6]}, \"" + item[2] + f"\")'>{text}</a></p></div>"
		output_string += news_item_string

	output_string += middle_string

	for item in health_records:
		border_class = "border-success" if item[6] else "border-danger"
		date_string = f"{item[1].day} {item[1]:%b} {item[1]:%Y}"
		text_class = "text-success" if item[6] else "text-danger"
		text = pub[item[6]].capitalize()
		
		health_item_string = f"<div class='card w-100 rounded my-3 px-3 py-2 text-dark {border_class}'><p class='card-text'>{item[2]}<br /><small class='text-muted'>{date_string}</small><a class='no-underline float-right {text_class}' href='#!' onclick='changePublish(2, {item[0]}, {item[6]}, \"" + item[2] + f"\")'>{text}</a></p></div>"

		output_string += health_item_string

	return output_string

# Change published status for an article
@app.post("/publish")
def change_publish():
	type = request.json["type"]
	issue = request.json["issue"]
	state = request.json["state"]
	title = request.json["title"]
	result = mysql_toggle_publish_status(type, issue, state, title)
	return result

# GENERAL FUNCTIONS

# MySQL connection
# Returns connection and cursor objects
def mysql_connect(prepared):
	connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DATABASE, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
	connection.set_charset_collation("utf8mb4", "utf8mb4_unicode_ci")
	cursor = connection.cursor(prepared)
	return (connection, cursor)
	
# MySQL insert new article
def mysql_insert(type, record):
	connection, cursor = mysql_connect(True)
	try:
		# connection, cursor = mysql_connect(True)
		sql_insert_query = ("""INSERT INTO `{0}` (`date`, `title`, `body`, `author`, `image`, `publish`) VALUES (%s,%s,%s,%s,%s,%s)""").format(type)
		result  = cursor.execute(sql_insert_query, record)
		connection.commit()
		return {"result" : 1, "message": "Success"}
	except Error as error:
		return {"result" : 0, "message": error}
	finally:
		# Close database connection
		if(connection.is_connected()):
			cursor.close()
			connection.close()

# MySQL toggle published status
def mysql_toggle_publish_status(type, issue, state, title):
	connection, cursor = mysql_connect(True)
	try:
		# connection, cursor = mysql_connect(True)
		type_string = types[type-1]
		new_state = (1, 0)[state] # Invert state
		update_tuple = (new_state, issue)
		sql_update_query = ("""UPDATE `{0}` SET `publish` = %s WHERE `issue` = %s""").format(type_string)
		result  = cursor.execute(sql_update_query, update_tuple)
		connection.commit()
		return {"result" : 1, "message": "Success"}
	except Error as error:
		return {"result" : 0, "message": error}
	finally:
		# Close database connection
		if(connection.is_connected()):
			cursor.close()
			connection.close()

# Parse body text to basic HTML (new lines and paragraphs)
def parse_to_html(text):
	# Add leading and trailing paragraph tags
	text = "<p>" + text + "</p>"
	# Use \n for newline on all systems
	text = re.sub(r"(\r\n|\n|\r)", r"\n", text)
	# Only allow two newlines in a row
	text = re.sub(r"\n\n+", r"\n\n", text)
	# Double newline -> paragraph
	text = text.replace("\n\n", "</p><p>")
	# Single newline -> break
	text = text.replace("\n", "<br />")
	return text

# Image processing
def process_image(im, size_tuple):
	# Process the Pillow/PIL image
	size = im.size
	if size == (700, 400):
		return im
	
	# Aspect fill algorithm
	width, height = size
	aspect_ratio = float(width) / float(height)
	width_ratio = size_tuple[0] / float(width)
	height_ratio = size_tuple[1] / float(height)
	best_ratio = max(width_ratio, height_ratio)
	new_width = int(width * best_ratio)
	new_height = int(height * best_ratio)
	im2 = im.resize((new_width, new_height))
	
	# Crop required area at centre
	# PIL origin is at top-left
	left = int((new_width - size_tuple[0]) / 2.0)
	right = int(left + size_tuple[0])
	top = int((new_height - size_tuple[1]) / 2.0)
	bottom = int(top + size_tuple[1])
	box = (left, top, right, bottom)
	im3 = im2.crop(box)
	
	# Logging
	string = f"Image size: w={width}, h={height}\nAspect Fill: w={new_width}, h={new_height}\nCrop box (LTRB): {left}, {top}, {right}, {bottom}\n"
	print(string)
	
	# Return final image
	return im3

# Run app
if os.environ.get('APP_LOCATION') == 'heroku':
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
