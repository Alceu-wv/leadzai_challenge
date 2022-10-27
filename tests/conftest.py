import pytest

from paginator_generator.error_handler import PaginationGeneratorErrorHandler
from paginator_generator.generator import PaginationGenerator

@pytest.fixture()
def error_handler():
    return PaginationGeneratorErrorHandler(current_page=2, total_pages=5, boundaries=2, around=0)

@pytest.fixture()
def paginator():
    return PaginationGenerator(current_page=1, total_pages=1, boundaries=0, around=0)