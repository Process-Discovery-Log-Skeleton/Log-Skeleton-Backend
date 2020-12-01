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

🚨 Install flake8 as for linting:

```pip install flake8 flake8-docstrings```


✅ Install pytest for unit testing.

  ```pip install pytest```

🌐 Install flask for the REST-API server.

  ```pip install flask```

📈 Install pm4py for some process discovery helpers.

  ```pip install pm4py```


#### Starting the API server

🚀 To start the application run:

  ```python -m src.api.server```

This command will start a HTTP server for the API.


#### Using the API

###### Endpoints:

```/log-skeleton```

This HTTP endpoint will accept an XES event log as the input and return a log-skeleton model based on that model.

Provide an XES event-log in the body of the request for the server.

###### Parameters:

- `noise-threshold`: Number between 0 and 1 to specitfy a _noise_threshold_ for the algorithm.
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

###### Error codes

In case of an error the API will respond with the appropriate HTTP error code. Further an error description will be provided in the response in the `error_msg` field.

###### Examples

The following example will return a log skeleton model for the given log in the body with a noise threshold of _3%_.
`https://<domain>/log-skeleton?noise-threshold=0.03`

The following example will return a log skeleton model for the given log in the body with a noise threshold of _3%_ and it will include the extended traces.
`https://<domain>/log-skeleton?noise-threshold=0.1&extended-trace=true`

The following example will return a _404_ error since there is no route called `/log-skleeton`.
`https://<domain>/log-skleeton?noise-threshold=0.1`
