[![Python package](https://github.com/spabst/next-fibo-service/actions/workflows/python-app.yml/badge.svg)](https://github.com/spabst/next-fibo-service/actions/workflows/python-app.yml)

# Fibonacci Service

The Fibonacci Service is a simple HTTP service written in Python that provides an endpoint to calculate the next Fibonacci number given a Fibonacci number as input. It allows users to choose between JSON or MessagePack for both input and output.

## Features

- Accepts Fibonacci number as input and outputs the next Fibonacci number.
- Supports both JSON and MessagePack formats for input and output.
- Utilizes `@lru_cache` for caching Fibonacci numbers to improve performance.

## Requirements

- Python 3.x
- Flask
- Flask-Testing
- msgpack (optional, required for MessagePack support)
- pydantic
- requests
- pytest-cov
- coverage-badge 

