import pytest

from paginator_generator.error_handler import (
    PaginationGeneratorError,
    PaginationGeneratorErrorHandler,
)


def test__check_short_total_pages(error_handler: PaginationGeneratorErrorHandler):
    result_to_assert = None

    error_handler.around = 10
    error_handler.boundaries = 10
    error_handler.total_pages = 19

    try:
        error_handler.check_for_input_errors()
    except PaginationGeneratorError as error:
        result_to_assert = error.args[0]

    assert (
        result_to_assert
        == "'boundaries' and 'around' sum cannot be greater than total pages."
    )


def test__check_current_page_out_of_range(
    error_handler: PaginationGeneratorErrorHandler,
):
    result_to_assert = None

    error_handler.total_pages = 19
    error_handler.current_page = 20

    try:
        error_handler.check_for_input_errors()
    except PaginationGeneratorError as error:
        result_to_assert = error.args[0]

    assert (
        result_to_assert == "'current_page' must be within the range of 'total_pages'."
    )
