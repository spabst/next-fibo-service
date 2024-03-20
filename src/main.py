from flask import Flask, request, jsonify
import msgpack
from functools import lru_cache
from pydantic import validate_arguments, ValidationError

app = Flask(__name__)

@lru_cache(maxsize=None)
@validate_arguments
def fibonacci(n: int):
        number1 = 1
        number2 = 1
        next_fibo = number1 + number2
        while next_fibo <= n:
            number1 = number2
            number2 = next_fibo
            next_fibo = number1 + number2

        return next_fibo


@app.route('/next_fibonacci', methods=['POST'])
def next_fibonacci():
    data = request.get_data()
    content_type = request.content_type

    # Check if the content type is JSON or MessagePack
    if content_type == 'application/json':
        input_data = request.json
    elif content_type == 'application/msgpack':
        input_data = msgpack.unpackb(data, raw=False)
    else:
        return jsonify({'error': 'Unsupported content type. Please use JSON or MessagePack.'}), 400

    try:
        n = input_data['n']
        next_fib = fibonacci(n + 1)
        output_data = {'n': next_fib}
    except KeyError:
        return jsonify({'error': 'Input data must contain the key "n".'}), 400
    except TypeError:
        return jsonify({'error': 'Input data must be a JSON object or MessagePack.'}), 400

    # Choose output format based on content type
    if content_type == 'application/json':
        return jsonify(output_data)
    elif content_type == 'application/msgpack':
        return msgpack.packb(output_data, use_bin_type=True)

if __name__ == '__main__':
    app.run(debug=True)