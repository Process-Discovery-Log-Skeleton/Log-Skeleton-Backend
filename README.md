<h1 align="center">Log-Skeleton-Backend</h1>

<h3 align="center"> Status </h3>

<p align="center">
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
  <img src="https://github.com/Process-Discover-Log-Skeleton/Log-Skeleton-Backend/workflows/Build/badge.svg?branch=development"/>
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
</p>


#### 📄 Documentation

The project provides a documentation in the [GitHub Wiki](https://github.com/Process-Discovery-Log-Skeleton/Log-Skeleton-Backend/wiki) page of this project. 

It covers different topics like:
- Implementation of the [Log-Skeleton algorithm](https://github.com/Process-Discovery-Log-Skeleton/Log-Skeleton-Backend/wiki/Log-Skeleton)
- [XES Importer](https://github.com/Process-Discovery-Log-Skeleton/Log-Skeleton-Backend/wiki/XES-Importer)
- [API setup & usage](https://github.com/Process-Discovery-Log-Skeleton/Log-Skeleton-Backend/wiki/API)

#### 👷‍♀️ Installation & Setup

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
  
➕ Install the missing requirements.
  
  ```pip install -r requirements.txt```


#### 🚀 Starting the API server

To start the application run:

  ```python -m src.api.server```

This command will start a HTTP server for the API.


#### 🌐 Using the API

###### 🎯 Endpoints:

```/event-log```

`POST`
This HTTP endpoint will accept a `.xes` and `.csv` file attached to the HTTP request. It will store the file 
on the server. The request will return an identifier which can be used to access the file in the 
```/log-skeleton``` endpoint. The file will be deleted as soon as nobody accesses the file for 1 hour.

###### 🔧 Parameters:

When uploading a `.csv` file two parameters are available:

- `case-id` (required): Name of the column that uniquely identifies traces/ cases
- `case-prefix` (optional): Prefix of the case-id that identifies trace identifiers.

###### Example:

Imagine a `CSV` having two identfier columns. `concept:name` and `case:concept:name`.
`concept:name` identifies activities and `case:concept:name` identifies traces.

In this case `case:concept:name` would be the `case-id` parameter and `case-prefix` would have the value `case:`.
This is because 

`case:` + `concept:name` = `case:concept:name` ⇔ `case-prefix`+ `activitiy-id` = `case-id`

###### ```/event-log/example```

`POST`
This HTTP endpoint provides a way to fetch the `running-example.xes` file without uploading the actual file.
The server will import the file from the local disk. 

###### ```/log-skeleton/<id>```

`POST`

This HTTP endpoint will accept an `id` as the input and return a log-skeleton model based on that model.

Use `/event-log` to register the event log in the server. The server will return an identifier for your event log. Use this as the parameter for `<id>`.

###### 🔧 Parameters:

- `noise-threshold`: Number between 0 and 1 to specitfy a _noise_threshold_ for the algorithm.
- `extended-trace`: Boolean value indicating whether the trace extension will be included or not.
- `forbidden`: A set of forbidden activies.
- `required`: A set of required activies.

###### 📦 The API-Response:

In case the API gets used as it is inteded to be, it will return a JSON object containing the log skeleton model, all occuring activities and the applied parameters:

The `log-skeleton` model contains the following fields:
- `always-after`: Contains a list of tuples representing the _always-after_ relationship.
- `always-before`: Contains a list of tuples representing the _always-before_ relationship.
- `equivalence`: Contains a list of tuples representing the _equivalence_ relationship.
- `never_together`: Contains a list of tuples representing the _never_together_ relationship.
- `next_one_way`: Contains a list of tuples representing the _next_one_way_ relationship.
- `next_both_ways`: Contains a list of tuples representing the _next_both_ways_ relationship.
- `counter`: Contains a JSON object representing the _counter_ relationships.

The `activities` list contains a list of all occuring activities in the event log.

- `parameters`: Contains a JSON object indicating the parameters applied and further information like IDs of the _trace start_ and _trace end_.

###### Example

```javascript

var res = await fetch('https:/<domain>/log-skeleton/d18213glk21')
var data = await res.json()

console.log(data)
```

```
{
  log-skeleton: {
    always-after: [...],
    always-before: [...],
    ...
  },
  activities: [
    "reinitate-request",
    "decide",
    ...
  ],
  parameters: {
    noise-thrshold: 0.03,
    extended-trace: true,
    ...
  }
}

```

###### ⛔️ Error codes

In case of an error the API will respond with the appropriate HTTP error code. Further an error description will be provided in the response in the `error_msg` field.

###### Common codes:

- `200`: OK
- `400`: BAD REQUEST, something is wrong with the request/ query
- `410`: MISSING RESOURCE, cannot find the provieded `event log id`

###### Examples
The following example will upload the attached `file` to the server. 
`https://<domain>/event-log`
The returned identifier will be `d18213glk21` throughout this example section.

The following example will return a log skeleton model for the given log in the body with a noise threshold of _3%_.
`https://<domain>/log-skeleton/d18213glk21?noise-threshold=0.03`

The following example will return a log skeleton model for the given log in the body with a noise threshold of _10%_ and it will include the extended traces.
`https://<domain>/log-skeleton/d18213glk21?noise-threshold=0.1&extended-trace=true`

The following example will return a _404_ error since there is no route called `/log-skleeton`.
`https://<domain>/log-skleeton/d18213glk21?noise-threshold=0.1`
