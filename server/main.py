"""
The main execution entry-point for the webapp/services.
"""

# Import system stuff
from flask import make_response

from server.command_center import app


@app.before_request
def before_request_callback():
    pass


@app.teardown_request
def teardown_request(exception):
    """Request teardown handlers, which are called when every request is completed"""
    pass


@app.after_request
def after_request_callback(response):
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)
