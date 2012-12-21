from flask import g
from flask import jsonify
import os

from command_center import app
from command_center.services.sensors import SensorService
from command_center.services.top import TopService


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