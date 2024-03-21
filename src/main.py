from flask import Flask, request, jsonify
from typing_extensions import Annotated
import msgpack
from functools import lru_cache
from pydantic import validate_call, Field, ValidationError
import warnings
app = Flask(__name__)

import math
 
# A utility function that returns true if x is perfect square
def is_perfect_square(x):
    s = int(math.sqrt(x))
    return s*s == x
 
# Returns true if n is a Fibonacci Number, else false
def is_fibonacci(n):
    return is_perfect_square(5*n*n + 4) or is_perfect_square(5*n*n - 4)

@lru_cache(maxsize=None)
@validate_call
def fibonacci(n: Annotated[int, Field(gt=0)]):
    if not is_fibonacci(n):
        warnings.warn(f'The provided number is not part of the fibonacci sequence. The code is providing the next number is the fibonacci sequence greater than {n}', Warning)
        #    raise ValueError("The provided number is not part of the fibonacci sequence. The code is providing the next number is the fibonacci sequence greater than the input value")
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
        next_fib = fibonacci(n)
        output_data = {'n': next_fib}
    except KeyError:
        return jsonify({'error': 'Input data must contain the key "n".'}), 400
    except TypeError:
        return jsonify({'error': 'Input data must be a JSON object or MessagePack.'}), 400
    except ValidationError as e:
        return jsonify({'error': e.errors()[0]['msg']}), 400

    # Choose output format based on content type
    if content_type == 'application/json':
        return jsonify(output_data)
    elif content_type == 'application/msgpack':
        return msgpack.packb(output_data, use_bin_type=True)

if __name__ == '__main__':
    app.run(debug=True, port=5200)