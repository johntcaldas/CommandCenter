from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, jsonify
import os
import sys

app = Flask(__name__)


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
    return render_template('main.html', theString = "Hello World!")


@app.route("/disks", methods=['GET'])
def disks():
    return render_template('disks.html')


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/system/sensors", methods=['GET'])
def sensors():
    sensors = os.popen('sensors')
    sensors_by_line = []
    for line in sensors.readlines():
        sensors_by_line.append(line)


    return jsonify({'success': True, 'result': sensors_by_line})


if __name__ == "__main__":
    app.run(debug=True)
