"""Implemenation of the REST-API endpoint."""
from flask import Flask

app = Flask(__name__)


@app.route('log-skeleton', methods=['GET'])
def log_skeleton():
    """Provide endpoint at /log-skeleton."""
    return 'Not implemented yet.'


app.run()
