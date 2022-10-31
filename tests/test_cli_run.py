import pytest

from main import input_integer, run
from paginator_generator.error_handler import PaginationGeneratorError
from paginator_generator.generator import PaginationGenerator

def test_input_integer_negative_number(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: "1")

    value = input_integer('value from cli')

    assert value == 1

def test_run(mocker):
    mocker.patch("main.input_integer")
    mocker.patch.object(PaginationGenerator, "__init__", return_value=None)
    mocker.patch.object(PaginationGenerator, "build_pagination")
    
    run()

