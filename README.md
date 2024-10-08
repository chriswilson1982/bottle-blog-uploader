# Bottle Blog Uploader

This is a simple web app for uploading new blog posts to a MySQL database.
It is used to update our practice website and can be found live at upload.churchviewmedicalpractice.com.

The app allows the entry of a title, author and body text, provides a timestamp and requires a password before submission. One of two different blogs can be selected (*Health Blog* and *News*). It prevents submission if an article with the same title already exists.

The body text area accepts HTML code, but newlines are detected automatically and a double newline will result in a new paragraph element automatically. There are shortcut buttons for adding HTML images and link code.

Images will be resized and cropped as needed to 700x400 pixels using an aspect fill algorithm.

Editing and deletion are not supported yet, though the published status of existing articles can be toggled. There is limited error handling, with error messages being displayed on the 'Submit' button.

The app is built using Python 3, Bottle, JavaScript, jQuery, HTML, CSS, Bootstrap and Font Awesome.
