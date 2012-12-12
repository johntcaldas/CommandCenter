"""
The main execution entry-point for the webapp/services.
"""

# Import system stuff
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, jsonify
import os

app = Flask(__name__)

#Import our stuff
from services.sensors import SensorService
from services.top import TopService

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


@app.route("/system/sensors", methods=['GET'])
def sensors():

    sensor_service = SensorService()
    sensor_data = sensor_service.get_sensor_data()


    return jsonify({
        'success': True,
        'cpu_temp': sensor_data['cpu_temp'],
        'mb_temp': sensor_data['mb_temp'],
        'vid_temp': sensor_data['vid_temp'],
        'sensors_by_line': sensor_data['sensors_by_line']
    })


@app.route("/system/top", methods=['GET'])
def system_top():
    top_service = TopService()
    top_data = top_service.get_top_data()

    return jsonify({
        'success': True,
        'first_line': top_data['first_line'],
        'header_by_line': top_data['header_by_line'],
        'column_names': top_data['column_names'],
        'rows': top_data['rows']
    })


@app.route("/system/date", methods=['GET'])
def system_date():
    date_handle = os.popen('date')
    date = date_handle.readline()

    return jsonify({'success': True,
                   'date': date})


if __name__ == "__main__":
    app.run(debug=True)
