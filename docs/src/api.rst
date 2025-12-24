.. _api_reference:

REST API Reference
==================

UMLX provides a complete FastAPI-based REST API for remote access to array operations
and machine learning functionality. The API runs on port 1023 by default.

Starting the API Server
------------------------

Command Line
^^^^^^^^^^^^

Start the API server using the command line:

.. code-block:: shell

    python -m mlx.api.server

Or using the installed entry point:

.. code-block:: shell

    mlx.api

With custom configuration:

.. code-block:: shell

    mlx.api --host 0.0.0.0 --port 1023 --reload

Python
^^^^^^

Start the server programmatically:

.. code-block:: python

    from mlx.api import start_server
    
    start_server(host="0.0.0.0", port=1023)

Interactive Documentation
-------------------------

Once the server is running, access interactive API documentation at:

- Swagger UI: ``http://localhost:1023/docs``
- ReDoc: ``http://localhost:1023/redoc``

API Endpoints
-------------

Health Check
^^^^^^^^^^^^

Check the API server health and available devices.

**GET** ``/health``

Response:

.. code-block:: json

    {
      "status": "healthy",
      "version": "0.30.3",
      "devices": ["cpu: available"]
    }

Array Operations
^^^^^^^^^^^^^^^^

Create Array
""""""""""""

Create a new MLX array.

**POST** ``/array/create``

Request body:

.. code-block:: json

    {
      "data": [1, 2, 3, 4],
      "dtype": "float32"
    }

Response:

.. code-block:: json

    {
      "shape": [4],
      "dtype": "float32",
      "size": 4,
      "ndim": 1
    }

Array Info
""""""""""

Get information about an array with given shape and dtype.

**GET** ``/array/info?shape=2,3&dtype=float32``

Response:

.. code-block:: json

    {
      "shape": [2, 3],
      "dtype": "float32",
      "size": 6,
      "ndim": 2
    }

Array Operation
"""""""""""""""

Perform binary operations on arrays.

**POST** ``/array/operation``

Request body:

.. code-block:: json

    {
      "operation": "add",
      "array1": [1, 2, 3],
      "array2": [4, 5, 6]
    }

Supported operations: ``add``, ``subtract``, ``multiply``, ``divide``, ``matmul``

Response:

.. code-block:: json

    {
      "result": [5, 7, 9],
      "shape": [3],
      "dtype": "int32"
    }

Device Management
^^^^^^^^^^^^^^^^^

Get Devices
"""""""""""

Query available devices.

**GET** ``/devices``

Response:

.. code-block:: json

    {
      "device_type": "cpu",
      "default_device": "cpu"
    }

Set Device
""""""""""

Set the default device for operations.

**POST** ``/device/set``

Request body:

.. code-block:: json

    {
      "device": "gpu"
    }

Response:

.. code-block:: json

    {
      "status": "success",
      "device": "gpu"
    }

Examples
--------

Python Client
^^^^^^^^^^^^^

Example using Python's ``requests`` library:

.. code-block:: python

    import requests
    
    # Create an array
    response = requests.post(
        "http://localhost:1023/array/create",
        json={"data": [1, 2, 3, 4], "dtype": "float32"}
    )
    print(response.json())
    
    # Perform operation
    response = requests.post(
        "http://localhost:1023/array/operation",
        json={
            "operation": "add",
            "array1": [1, 2, 3],
            "array2": [4, 5, 6]
        }
    )
    print(response.json())

cURL
^^^^

Example using cURL:

.. code-block:: shell

    # Health check
    curl http://localhost:1023/health
    
    # Create array
    curl -X POST http://localhost:1023/array/create \
      -H "Content-Type: application/json" \
      -d '{"data": [1, 2, 3, 4], "dtype": "float32"}'
    
    # Array operation
    curl -X POST http://localhost:1023/array/operation \
      -H "Content-Type: application/json" \
      -d '{"operation": "add", "array1": [1,2,3], "array2": [4,5,6]}'

Configuration
-------------

Port Configuration
^^^^^^^^^^^^^^^^^^

The default port is 1023. To use a different port:

.. code-block:: shell

    mlx.api --port 8080

Host Binding
^^^^^^^^^^^^

By default, the server binds to ``0.0.0.0`` (all interfaces). To bind to localhost only:

.. code-block:: shell

    mlx.api --host 127.0.0.1

Development Mode
^^^^^^^^^^^^^^^^

Enable auto-reload for development:

.. code-block:: shell

    mlx.api --reload

Security Considerations
-----------------------

- The API does not include authentication by default
- Consider using a reverse proxy (nginx, Apache) for production deployments
- Use HTTPS in production environments
- Implement rate limiting for public-facing deployments
- Run with appropriate user permissions (not root)

Performance
-----------

- The API uses async/await for concurrent request handling
- Array operations are performed using MLX's efficient backend
- Consider the network overhead for large array transfers
- Use batch operations where possible for better performance
