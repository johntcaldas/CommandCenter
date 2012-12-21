"""
The main execution entry-point for the webapp/services.
"""

# Import system stuff
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, jsonify

from command_center import app


@app.before_request
def before_request_callback():
    pass


@app.teardown_request
def teardown_request(exception):
    """Request teardown handlers, which are called when every request is completed"""
    pass


@app.after_request
def after_request_callback(response):
    return response


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', theString = "Hello World!")


@app.route("/disks", methods=['GET'])
def disks():
    return render_template('disks.html')


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
