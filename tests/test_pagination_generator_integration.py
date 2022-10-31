import pytest

from paginator_generator.error_handler import PaginationGeneratorError
from paginator_generator.generator import PaginationGenerator


def test_big_interval(paginator: PaginationGenerator):
    paginator.total_pages = 1000
    paginator.current_page = 800
    paginator.boundaries = 3
    paginator.around = 0

    assert paginator.build_pagination() == [1, 2, 3, "...", 800, "...", 998, 999, 1000]


def test_short_interval(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 1
    paginator.around = 0

    assert paginator.build_pagination() == [1, "...", 3, "...", 5]


def test_big_range_no_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 1000
    paginator.current_page = 800
    paginator.boundaries = 0
    paginator.around = 3

    assert paginator.build_pagination() == [797, 798, 799, 800, 801, 802, 803]


def test_short_range_no_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 0
    paginator.around = 2

    assert paginator.build_pagination() == [1, 2, 3, 4, 5]


def test_overlaping_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 4
    paginator.around = 0

    assert paginator.build_pagination() == [1, 2, 3, 4, 5]


def test_overlaping_boundaries_and_around(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 3
    paginator.around = 2

    assert paginator.build_pagination() == [1, 2, 3, 4, 5]


def test_around_or_boundaries_greater_than_total_pages():
    result_to_assert = None

    try:
        PaginationGenerator(current_page=3, total_pages=5, boundaries=3, around=3)
    except PaginationGeneratorError as error:
        result_to_assert = error.args[0]

    assert (
        result_to_assert
        == "'boundaries' and 'around' sum cannot be greater than total pages."
    )


def test_current_page_zero(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 0
    paginator.boundaries = 1
    paginator.around = 1

    assert paginator.build_pagination() == [1, "...", 5]


def test_total_pages_zero(paginator: PaginationGenerator):
    paginator.total_pages = 0
    paginator.current_page = 0
    paginator.boundaries = 1
    paginator.around = 1

    assert paginator.build_pagination() == []


def test_boundaries_zero(paginator: PaginationGenerator):
    paginator.total_pages = 10
    paginator.current_page = 10
    paginator.boundaries = 0
    paginator.around = 1

    assert paginator.build_pagination() == [9, 10]


def test_aroud_zero(paginator: PaginationGenerator):
    paginator.total_pages = 10
    paginator.current_page = 10
    paginator.boundaries = 1
    paginator.around = 0

    assert paginator.build_pagination() == [1, "...", 10]
