from collections import deque

import pytest

from paginator_generator.generator import PaginationGenerator


def test_big_interval(paginator: PaginationGenerator):
    paginator.total_pages = 1000
    paginator.current_page = 800
    paginator.boundaries = 3
    paginator.around = 0

    assert paginator.build_pagination() == deque(
        [1, 2, 3, "...", 800, "...", 998, 999, 1000]
    )


def test_short_interval(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 1
    paginator.around = 0

    assert paginator.build_pagination() == deque([1, "...", 3, "...", 5])


def test_big_range_no_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 1000
    paginator.current_page = 800
    paginator.boundaries = 0
    paginator.around = 3

    assert paginator.build_pagination() == deque(
        ["...", 797, 798, 799, 800, 801, 802, 803, "..."]
    )


def test_short_range_no_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 0
    paginator.around = 2

    assert paginator.build_pagination() == deque([1, 2, 3, 4, 5])


def test_overlaping_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 4
    paginator.around = 0

    assert paginator.build_pagination() == deque([1, 2, 3, 4, 5])


def test_overlaping_boundaries_and_around(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 3
    paginator.boundaries = 3
    paginator.around = 2

    assert paginator.build_pagination() == deque([1, 2, 3, 4, 5])


def test_around_or_boundaries_greater_than_total_pages():
    result = PaginationGenerator(
        current_page=3, total_pages=5, boundaries=3, around=3
    ).build_pagination()
    assert result == deque([1, 2, 3, 4, 5])


def test_current_page_zero(paginator: PaginationGenerator):
    paginator.total_pages = 5
    paginator.current_page = 0
    paginator.boundaries = 1
    paginator.around = 1

    assert paginator.build_pagination() == deque([1, "...", 5])


def test_total_pages_zero(paginator: PaginationGenerator):
    paginator.total_pages = 0
    paginator.current_page = 0
    paginator.boundaries = 1
    paginator.around = 1

    assert paginator.build_pagination() == deque([0])


def test_boundaries_zero(paginator: PaginationGenerator):
    paginator.total_pages = 10
    paginator.current_page = 10
    paginator.boundaries = 0
    paginator.around = 1

    assert paginator.build_pagination() == deque(["...", 9, 10])


def test_around_zero(paginator: PaginationGenerator):
    paginator.total_pages = 10
    paginator.current_page = 10
    paginator.boundaries = 1
    paginator.around = 0

    assert paginator.build_pagination() == deque([1, "...", 10])


def test_very_short(paginator: PaginationGenerator):
    paginator.total_pages = 1
    paginator.current_page = 1
    paginator.boundaries = 0
    paginator.around = 0

    assert paginator.build_pagination() == deque([1])


def test_very_short_last_page(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 2
    paginator.boundaries = 0
    paginator.around = 0

    assert paginator.build_pagination() == deque(["...", 2])


def test_very_short_first_page(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 1
    paginator.boundaries = 0
    paginator.around = 0

    assert paginator.build_pagination() == deque([1, "..."])


def test_very_short_with_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 1
    paginator.boundaries = 1
    paginator.around = 0

    assert paginator.build_pagination() == deque([1, 2])


def test_very_short_with_around(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 1
    paginator.boundaries = 2
    paginator.around = 1

    assert paginator.build_pagination() == deque([1, 2])


def test_very_short_with_big_around(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 1
    paginator.boundaries = 2
    paginator.around = 777

    assert paginator.build_pagination() == deque([1, 2])


def test_very_short_with_big_boundaries(paginator: PaginationGenerator):
    paginator.total_pages = 2
    paginator.current_page = 1
    paginator.boundaries = 2
    paginator.around = 777

    assert paginator.build_pagination() == deque([1, 2])


def test_all_zero(paginator: PaginationGenerator):
    paginator.total_pages = 0
    paginator.current_page = 0
    paginator.boundaries = 0
    paginator.around = 0

    assert paginator.build_pagination() == deque([0])


def test_all_huge_total_pages(paginator: PaginationGenerator):
    paginator.total_pages = 1000000000
    paginator.current_page = 500
    paginator.boundaries = 5
    paginator.around = 5

    assert paginator.build_pagination() == deque(
        [
            1,
            2,
            3,
            4,
            5,
            "...",
            495,
            496,
            497,
            498,
            499,
            500,
            501,
            502,
            503,
            504,
            505,
            "...",
            999999996,
            999999997,
            999999998,
            999999999,
            1000000000,
        ]
    )
