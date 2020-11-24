<h1 align="center">Log-Skeleton-Backend</h1>

<h3 align="center"> Status </h3>

<p align="center">
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
  <img src="https://github.com/Process-Discover-Log-Skeleton/Log-Skeleton-Backend/workflows/Build/badge.svg?branch=development"/>
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/Process-Discover-Log-Skeleton/Log-Skeleton-Backend">
</p>


### Installation & Setup

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


### Starting the REST-API server

🚀 To start the application run:

  ```python /src/api/server.py```

This command will start a HTTP server for the REST-API.


### Using the REST-API

**Endpoints:**

```/log-skeleton```

This HTTP endpoint will accept an XES event log as the input and return a log-skeleton model based on that model.

🏗 *Warning! The endpoint is currently developed.*