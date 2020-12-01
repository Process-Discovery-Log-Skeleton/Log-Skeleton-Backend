<h1 align="center">Log-Skeleton-Backend</h1>

<h3 align="center"> Status </h3>

<p align="center">
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
  <img src="https://github.com/Process-Discover-Log-Skeleton/Log-Skeleton-Backend/workflows/Build/badge.svg?branch=development"/>
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
</p>


#### Installation & Setup

This project requires python version < 3.9.x (some requirements are not compatible with 3.9.x).

To install the required dependencies use the following commands:

🐍 Download and install python 3 (lower than python 3.9).

🚨 Install a python linter:

```pip install flake8 flake8-docstrings```


✅ Install pytest for unit testing.

  ```pip install pytest```

🌐 Install flask for the REST-API server.

  ```pip install flask```

📈 Install pm4py for some process discovery helpers.

  ```pip install pm4py```


#### Starting the API server

🚀 To start the application run:

  ```python -m src.api.server.py```

This command will start a HTTP server for the API.


#### Using the API

###### Endpoints:

```/log-skeleton```

This HTTP endpoint will accept an XES event log as the input and return a log-skeleton model based on that model.

Provide an XES event-log in the body of the request for the server.

###### Parameters:

- `noise-thrshold`: Number between 0 and 1 to specitfy a _noise_threshold_ for the algorithm.
- `extended-trace`: Boolean value indicating whether the trace extension will be included or not.

###### The API-Response:

In case the API gets used as it is inteded to be, it will return a JSON object containing the following items:

- `always-after`: Contains a list of tuples representing the _always-after_ relationship.
- `always-before`: Contains a list of tuples representing the _always-before_ relationship.
- `equivalence`: Contains a list of tuples representing the _equivalence_ relationship.
- `never_together`: Contains a list of tuples representing the _never_together_ relationship.
- `next_one_way`: Contains a list of tuples representing the _next_one_way_ relationship.
- `next_both_ways`: Contains a list of tuples representing the _next_both_ways_ relationship.
- `counter`: Contains a JSON object representing the _counter_ relationships.
- `parameters`: Contains a JSON object indicating the parameters applied and further information like IDs of the _trace start_ and _trace end_.

