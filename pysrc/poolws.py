# Flask pool control web service
#
import subprocess
from flask import Flask
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

import poollib as poollib

import hwlib as hwlib
app = Flask(__name__)

# Send http header telling the browser to allow cross domain scripting
#   Code complements of: http://flask.pocoo.org/snippets/56/
#
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/health',methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')    
def health():
    s = hwlib.getCpuTemp();
    return 'CPU Temp is ' + str(s)

# Rotate filter valve to vacuum
#
@app.route('/vacuum',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def filter_valve_to_vacuum():
    poollib.filter_valve_to_vacuum()
    return 'rotating to vacuum'

# Rotate filter valve to skimmer
#    
@app.route('/skimmer',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def filter_valve_to_skimmer():
    poollib.filter_valve_to_skimmer()
    return 'rotating to skimmer'

# Rotate function valve to clean/filter
#
@app.route('/function-filter',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def function_valve_to_filter():
    poollib.function_valve_to_filter()
    return 'rotating function valve to filter'

# Rotate function valve to waterfall
#    
@app.route('/function-waterfall',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def function_valve_to_waterfall():
    poollib.function_valve_to_waterfall()
    return 'rotating function valve to waterfall'


# Enable manual operation
#
@app.route('/filtervalveon',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def filter_valve_on():
    poollib.filter_valve_on()
    return 'rotating to vacuum'
    
# Disable manual operation
#
@app.route('/filtervalveoff',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def filter_valve_off():
    poollib.filter_valve_off()
    return 'rotating to skimmer'

################################### Lighting ###############################

# Light 0 on
#
@app.route('/light0-on',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light0_on():
    subprocess.check_output(["light0-on"], stderr=subprocess.STDOUT)
    return 'light 0 on'

# Light 0 off
#
@app.route('/light0-off',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light0_off():
    subprocess.check_output(["light0-off"], stderr=subprocess.STDOUT)
    return 'light 0 off'

# Light 1 on
#
@app.route('/light1-on',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light1_on():
    subprocess.check_output(["light1-on"], stderr=subprocess.STDOUT)
    return 'light 1 on'

# Light 1 off
#
@app.route('/light1-off',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light1_off():
    subprocess.check_output(["light1-off"], stderr=subprocess.STDOUT)
    return 'light 1 off'
    
# Light 2 on
#
@app.route('/light2-on',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light2_on():
    subprocess.check_output(["light2-on"], stderr=subprocess.STDOUT)
    return 'light 2 on'

# Light 2 off
#
@app.route('/light2-off',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def light2_off():
    subprocess.check_output(["light2-off"], stderr=subprocess.STDOUT)
    return 'light 2 off'
    
# Light all on
#
@app.route('/lightall-on',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def lightall_on():
    poollib.lightall_on()
    return 'light all on'

# Light all off
#
@app.route('/lightall-off',methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')    
def lightall_off():
    poollib.lightall_off()
    return 'light all off'
    
    
    