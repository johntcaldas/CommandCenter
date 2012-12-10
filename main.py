"""
The main execution entry-point for the webapp/services.
"""

# Import system stuff
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, jsonify

app = Flask(__name__)

#Import our stuff
from services.sensors import SensorService

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

    sensor_service = SensorService()
    sensor_data = sensor_service.get_sensor_data()


    return jsonify({'success': True,
                    'cpu_temp': sensor_data['cpu_temp'],
                    'mb_temp': sensor_data['mb_temp'],
                    'vid_temp': sensor_data['vid_temp'],
                    'sensor_data': sensor_data['sensor_data']})


if __name__ == "__main__":
    app.run(debug=True)