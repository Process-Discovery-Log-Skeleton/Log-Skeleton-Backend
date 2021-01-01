"""Implemenation of the REST-API endpoint."""

from os import register_at_fork
from flask import Flask, request, jsonify
from src.components.logic.log_skeleton import Log_Skeleton
from src.components.util.xes_importer \
    import XES_Importer, TRACE_START, TRACE_END
from src.components.util.event_store import *
from flask_cors import CORS, cross_origin


PARAMETERS = 'parameters'
LOG_SKELETON = 'model'
ACTIVITIES = 'activities'

# HTTP Methods
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'
POST = 'POST'

# Http status codes
__OK__ = 200
__BAD_REQUEST__ = 400
__MISSING_RESOURCE__ = 410

# Http query strings/ defaul values
__NOISE_THRESHOLD__ = 'noiseThreshold'
__NOISE_THRESHOLD_DEFAULT__ = 0.0
FORBIDDEN = 'forbidden'
REQUIRED = 'required'

__EXTENDED_TRACE__ = 'extended-trace'
__EXTENDED_TRACE_DEFAULT__ = False

ID = 'id'
EVENT_LOG = 'event-log'
FILE = 'file'

ALLOWED_EXTENSIONS = {'xes', 'csv'}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

importer = XES_Importer()

app.secret_key = "my secret key"


def allowed_file(filename):
    """Determine whether the file is allowed.

    This is necessary to prevent cross-site-scripting.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/event-log/example', methods=['GET', 'POST'])
@cross_origin()
def event_log_example():

    content = pull_event_log('example')

    importer = XES_Importer()

    log, activities, filtered = \
            importer.import_str(content, [], [], extended_trace=False)

    return jsonify({
        'id': 'example',
        'activities': list(activities)
    })


@app.route('/event-log', methods=['GET', 'POST'])
@cross_origin()
def event_log():
    """Endpoint for uploading XES files."""
    method = request.method

    id = request.args.get(ID)

    if method == POST:
        if FILE not in request.files:
            return jsonify({'error': "No selected file"}), __BAD_REQUEST__
        file = request.files[FILE]
        if file.filename == '':
            return jsonify({'error': "Empty files"}), __BAD_REQUEST__

        if not allowed_file(file.filename):
            return jsonify({
                'error': "File type not supported"
            }), __BAD_REQUEST__

        id = put_event_log(file)

        importer = XES_Importer()

        try:
            content = pull_event_log(id)

            log, activities, filtered = \
                importer.import_str(content, [], [], extended_trace=False)

            return jsonify({
                'id': id,
                'activities': list(activities)
            })
        except:  # noqa: E722
            return jsonify({
                'error': "Could not import file."
            }), __BAD_REQUEST__

    return jsonify({'error': "Something is wrong"})


@app.route('/log-skeleton/<id>', methods=['GET', 'POST'])
# @cross_origin()
def log_skeleton(id):
    """Provide endpoint at /log-skeleton."""
    result, code = apply(id, request)

    response = jsonify(result)

    return response, code


def str_to_bool(value):
    """Convert a string value to bool.

    True in case:
        - 'true'
        - 1
    False in case:
        - 'false'
        - 0
    """
    b = value.lower()

    if b == 'true' or b == '1':
        return True

    if b == 'false' or b == '0':
        return False

    return __EXTENDED_TRACE_DEFAULT__


def apply(id, req):
    """Apply the log-skeleton algo to the input.

    Returns a tuple containing the result in the first place
    and the http-code in the second.

    Example:
        result, code: apply(request)
    """
    noise_para = req.args.get(__NOISE_THRESHOLD__)
    trace_para = req.args.get(__EXTENDED_TRACE__)

    noise_threshold = __NOISE_THRESHOLD_DEFAULT__
    include_extended_traces = __EXTENDED_TRACE_DEFAULT__

    forbidden = req.args.getlist(FORBIDDEN)
    required = req.args.getlist(REQUIRED)

    # Extract noise_threshold parameter
    if noise_para is not None:
        try:
            noise_threshold = float(noise_para)
        except:  # noqa: E722
            return {
                'error': __NOISE_THRESHOLD__ +
                ' parameter must be a number (between 0 and 1) value!'
            }, __BAD_REQUEST__

    # Extract extended traces parameter
    if trace_para is not None:
        try:
            include_extended_traces = str_to_bool(trace_para)
        except:  # noqa: E722
            return {
                'error': __EXTENDED_TRACE__ +
                ' parameter must be a boolean value!'
            }, __BAD_REQUEST__

    if forbidden is None:
        forbidden = []

    if required is None:
        required = []

    try:
        content = pull_event_log(id)

        log, all_activities, filtered = \
            importer.import_str(content,
                                forbidden,
                                required,
                                extended_trace=include_extended_traces)

    except (EventLogNotFoundError, KeyError):
        return {
            'error': 'Cannot find the event log.'
        }, __MISSING_RESOURCE__
    except:  # noqa: E722
        return {'error': 'Unable to import XES log. \
                             Either the log is invalid  \
                             or the id is not currect'}, \
            __BAD_REQUEST__

    lsk_algorithm = Log_Skeleton(log, filtered,
                                 noise_threshold,
                                 include_extended_traces)

    model = lsk_algorithm.apply()

    result = {
        LOG_SKELETON: model,
        ACTIVITIES: all_activities,
        PARAMETERS: {
            __NOISE_THRESHOLD__: lsk_algorithm.noise_threshold,
            __EXTENDED_TRACE__: include_extended_traces,
            FORBIDDEN: forbidden,
            REQUIRED: required
        }
    }

    if include_extended_traces:
        # Send the CONCEPT:NAME of the trace start/ end to the user
        result[PARAMETERS]['trace-start'] = \
            importer.activity_concept_name(TRACE_START)
        result[PARAMETERS]['trace-end'] = \
            importer.activity_concept_name(TRACE_END)

    return result, __OK__


# event_store.start_event_store()
# app.run()
if __name__ == "__main__":
    print('Server running!...')
    app.run(debug=True, host='0.0.0.0')
