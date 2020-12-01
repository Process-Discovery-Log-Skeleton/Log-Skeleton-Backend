"""Implemenation of the REST-API endpoint."""

from flask import Flask, request, jsonify
from flask import json
from src.components.logic.log_skeleton import Log_Skeleton
from src.components.util.xes_importer import XES_Importer

# Http status codes
__OK__ = 200
__BAD_REQUEST__ = 400

# Http query strings/ defaul values
__NOISE_THRESHOLD__ = 'noise-threshold'
__NOISE_THRESHOLD_DEFAULT__ = 0.0

app = Flask(__name__)
importer = XES_Importer()

@app.route('/log-skeleton', methods=['GET'])
def log_skeleton():
    """Provide endpoint at /log-skeleton."""
    result, code = apply(request)

    response = jsonify(result)

    return response, code

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

    noise_threshold = req.args.get(__NOISE_THRESHOLD__)

    if noise_threshold is None:
        noise_threshold = __NOISE_THRESHOLD_DEFAULT__
    
    lsk_algorithm = Log_Skeleton(log, activities, noise_threshold)

    model = lsk_algorithm.apply()

    return model, __OK__


app.run()
