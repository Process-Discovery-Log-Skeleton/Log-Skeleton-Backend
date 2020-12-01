"""Implemenation of the REST-API endpoint."""

from flask import Flask, request, jsonify
from flask import json
from src.components.logic.log_skeleton import Log_Skeleton
from src.components.util.xes_importer import *

__PARAMETERS__ = 'parameters'

# Http status codes
__OK__ = 200
__BAD_REQUEST__ = 400

# Http query strings/ defaul values
__NOISE_THRESHOLD__ = 'noise-threshold'
__NOISE_THRESHOLD_DEFAULT__ = 0.0

__EXTENDED_TRACE__ = 'extended-trace'
__EXTENDED_TRACE_DEFAULT__ = False

app = Flask(__name__)
importer = XES_Importer()

@app.route('/log-skeleton', methods=['GET'])
def log_skeleton():
    """Provide endpoint at /log-skeleton."""
    result, code = apply(request)

    response = jsonify(result)

    return response, code

def strToBool(value):
    b = value.lower()

    if b == 'true' or \
       b == '1':
       return True

    if b == 'false' or \
       b == '0':
       return False

    return __EXTENDED_TRACE_DEFAULT__


def apply(req):
    """Apply the log-skeleton algo to the input.
    
    Returns a tuple containing the result in the first place
    and the http-code in the second.

    Example:
        result, code: apply(request)
    """
    try:
        log, activities = importer.import_http_query(req)
    except:
        return {'error_msg': """Unable to import XES log.
                             Check your log on synax error"""}, \
                __BAD_REQUEST__

    noise_para = req.args.get(__NOISE_THRESHOLD__)
    trace_para = req.args.get(__EXTENDED_TRACE__)

    noise_threshold = __NOISE_THRESHOLD_DEFAULT__
    include_extended_traces = __EXTENDED_TRACE_DEFAULT__
    
    # Extract noise_threshold parameter
    if not noise_para is None:
        try:
            noise_threshold = float(noise_para)
        except:
            return {
                'error_msg': __NOISE_THRESHOLD__ + 
                ' parameter must be a number (between 0 and 1) value!'
            }, __BAD_REQUEST__

    # Extract extended traces parameter
    if not trace_para is None:
        try:
            include_extended_traces = strToBool(trace_para)
        except:
            return {
                'error_msg': __EXTENDED_TRACE__ + 
                ' parameter must be a boolean value!'
            }, __BAD_REQUEST__
    
    lsk_algorithm = Log_Skeleton(log, activities, noise_threshold)

    model = lsk_algorithm.apply()

    model[__PARAMETERS__] = {
        __NOISE_THRESHOLD__: lsk_algorithm.noise_threshold,
        __EXTENDED_TRACE__: include_extended_traces
    }

    if include_extended_traces:
        # Send the CONCEPT:NAME of the trace start/ end to the user
        model[__PARAMETERS__]['trace-start'] = \
            importer.activity_concept_name(TRACE_START)
        model[__PARAMETERS__]['trace-end'] = \
            importer.activity_concept_name(TRACE_END)

    return model, __OK__


app.run()
