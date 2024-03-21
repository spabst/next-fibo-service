import pytest
from pydantic import ValidationError
import warnings
from src.main import fibonacci


def test_fibonacci_sequence():
    # Test Fibonacci sequence generation
    assert fibonacci(1) == 2
    assert fibonacci(2) == 3
    assert fibonacci(3) == 5
    assert fibonacci(5) == 8
    assert fibonacci(8) == 13
    assert fibonacci(13) == 21
    assert fibonacci(21) == 34


def test_invalid_inputs():
    # Test invalid inputs
    with pytest.raises(ValidationError):
        fibonacci('string')
    with pytest.raises(ValidationError):
        fibonacci(3.14)
    with pytest.raises(ValidationError):
        fibonacci(-1)
    with pytest.raises(ValidationError):
        fibonacci(0)
    for i in [4, 6, 7, 9, 12, 14, 15]:
        with warnings.catch_warnings(record=True) as w:
            # Cause the warning to be issued
            fibonacci(i)

            # Check if any warning was issued
            assert len(w) == 1
            # Check the message of the warning
            assert issubclass(w[0].category, Warning)
            assert "The provided number is not part of the fibonacci sequence" in str(w[0].message)
