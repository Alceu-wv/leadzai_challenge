import pytest

from paginator_generator.error_handler import PaginationGeneratorErrorHandler

def test_instanciate(error_handler):
    
    assert isinstance(error_handler, PaginationGeneratorErrorHandler)

def test__check_short_total_pages():
    pass

def test__check_current_page_out_of_range():
    pass

def test_check_for_input_errors():
    pass



