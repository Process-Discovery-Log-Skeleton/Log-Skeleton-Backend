"""Implemenation of the REST-API endpoint."""

from flask import Flask, request, jsonify, flash
from src.components.logic.log_skeleton import Log_Skeleton
from src.components.util.xes_importer \
    import XES_Importer, TRACE_START, TRACE_END
import src.components.util.event_store as event_store

__PARAMETERS__ = 'parameters'

# HTTP Methods
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'
POST = 'POST'

# Http status codes
__OK__ = 200
__BAD_REQUEST__ = 400

# Http query strings/ defaul values
__NOISE_THRESHOLD__ = 'noise-threshold'
__NOISE_THRESHOLD_DEFAULT__ = 0.0
__FORBIDDEN__ = 'forbidden'
__REQUIRED__ = 'required'

__EXTENDED_TRACE__ = 'extended-trace'
__EXTENDED_TRACE_DEFAULT__ = False

ID = 'id'
EVENT_LOG = 'event-log'
FILE = 'file'

ALLOWED_EXTENSIONS = {'.xes'}

app = Flask(__name__)
importer = XES_Importer()


def allowed_file(filename):
    """Determine whether the file is allowed.

    This is necessary to prevent cross-site-scripting.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/event-log', methods=['GET', 'POST', 'DELETE'])
def event_log():
    """Endpoint for uploading XES files."""
    method = request.method

    id = request.args.get(ID)

    if method == POST:
        if FILE not in request.files:
            flash('No selected file')
            return
        file = request.files[FILE]

        if file.filename == '':
            flash('No selected file')
            return

        if allowed_file(file.filename):
            flash('Type of file not supported.')
            return

        id = event_store.put_event_log(file)

        return id


@app.route('/log-skeleton/<id>', methods=['GET', 'POST'])
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

    forbidden = req.args.getlist(__FORBIDDEN__)
    required = req.args.getlist(__REQUIRED__)

    # Extract noise_threshold parameter
    if noise_para is not None:
        try:
            noise_threshold = float(noise_para)
        except:  # noqa: E722
            return {
                'error_msg': __NOISE_THRESHOLD__ +
                ' parameter must be a number (between 0 and 1) value!'
            }, __BAD_REQUEST__

    # Extract extended traces parameter
    if trace_para is not None:
        try:
            include_extended_traces = str_to_bool(trace_para)
        except:  # noqa: E722
            return {
                'error_msg': __EXTENDED_TRACE__ +
                ' parameter must be a boolean value!'
            }, __BAD_REQUEST__

    if forbidden is None:
        forbidden = []

    if required is None:
        required = []

    try:
        path = event_store.pull_event_log(id)

        log, all_activities = \
            importer.import_file(path,
                                 forbidden,
                                 required,
                                 extended_trace=include_extended_traces)
    except:  # noqa: E722
        return {'error_msg': 'Unable to import XES log. \
                             Either the log is invalid  \
                             or the id is not currect'}, \
            __BAD_REQUEST__

    lsk_algorithm = Log_Skeleton(log, all_activities,
                                 noise_threshold,
                                 include_extended_traces)

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


# event_store.start_event_store()
app.run()
