[![Python package](https://github.com/spabst/next-fibo-service/actions/workflows/python-app.yml/badge.svg)](https://github.com/spabst/next-fibo-service/actions/workflows/python-app.yml)

# Fibonacci Service

The Fibonacci Service is a simple HTTP service written in Python that provides an endpoint to calculate the next Fibonacci number given a Fibonacci number as input. It allows users to choose between JSON or MessagePack for both input and output.

## Features

- Accepts Fibonacci number as input and outputs the next Fibonacci number.
- Supports both JSON and MessagePack formats for input and output.
- Utilizes `@lru_cache` for caching Fibonacci numbers to improve performance.

## Assumptions
According to Wikipedia, the fibonacci sequence usually starts with 0 and 1, but Fibonacci himself was starting the sequence with 1 and 2. In the current code, we raise an error for an input value of 0 to honor autor of the sequence.
When the number provided doesn't match a fibonacci number, the code raises a warning, but still provide the closest upper fibonacci number.
The code accept both JSON and MessagePack. When you send the message in a specific content-type, you get a response with the same content-type.

## Future Improvements:
- add the coverage badge to the current Readme file
- dockerize the application and automate the build via the pipeline. Push the result to a plubic registry
- add a load test to verify if the cache is actually impoving the performances of the service and if cache configuration is sufficient.
- split dependencies in a dev and a prod file. Move pytest and packages related to testing to the dev requirements. 


## Requirements

- Python 3.x
- Flask
- Flask-Testing
- msgpack (optional, required for MessagePack support)
- pydantic
- requests
- pytest-cov
- coverage-badge


## Installation
to run the code on your machine
1. Clone the repository:
```
git clone https://github.com/spabst/next-fibo-service.git
```
2. Navigate to the folder:
```
cd next-fibo-service
```
3. Install the dependencies (please consider creating and activating a virtual environment for the purpose):
```
python -m pip install -r requirements.txt
```
4. Run the code:
```
python src/main.py
```
5. Send POST requests to the endpoint `http://localhost:5200/next_fibonacci` with the Fibonacci number as input in either JSON or MessagePack format. For example:
```
curl -X POST -H "Content-Type: application/json" -d '{"n": 34}' http://localhost:5200/next_fibonacci
```


## Run the tests:
You can run tests through pytest with the following command:

```
pytest
```

If you want to visualize the code coverage, you can run the following pytest-cov command to run the tests and display coverage recap

```
pytest --cov
```
Or, if you prefer a detailed analysis, you can generate an html with more detailed and browsable information:
```
pytest --cov --cov-report=html:coverage_re
```
