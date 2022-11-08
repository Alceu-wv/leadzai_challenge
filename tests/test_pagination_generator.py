from collections import deque
from unittest.mock import MagicMock

import pytest

from paginator_generator.generator import PaginationGenerator


@pytest.mark.parametrize(
    "boundaries, result_to_assert",
    (
        (1, deque([1])),
        (2, deque([1, 2])),
        (3, deque([1, 2, 3])),
    ),
)
def test__get_beggining(paginator: PaginationGenerator, boundaries, result_to_assert):
    paginator.boundaries = boundaries

    result = paginator._get_beggining()

    assert isinstance(result, deque)
    assert result == result_to_assert
    assert len(result) == paginator.boundaries


@pytest.mark.parametrize(
    "current_page, around, result_to_assert",
    (
        (10, 1, deque([9, 10])),
        (10, 2, deque([8, 9, 10])),
        (10, 3, deque([7, 8, 9, 10])),
    ),
)
def test__get_middle(
    paginator: PaginationGenerator, current_page, around, result_to_assert
):
    paginator.around = around
    paginator.current_page = current_page
    paginator.total_pages = 10

    result = paginator._get_middle()

    assert isinstance(result, deque)
    assert result == result_to_assert
    assert len(result) == around + 1


@pytest.mark.parametrize(
    "pages, boundaries, result_to_assert",
    (
        (10, 1, deque([10])),
        (10, 2, deque([9, 10])),
        (10, 3, deque([8, 9, 10])),
    ),
)
def test__get_end(paginator: PaginationGenerator, pages, boundaries, result_to_assert):
    paginator.boundaries = boundaries
    paginator.total_pages = pages

    result = paginator._get_end()

    assert isinstance(result, deque)
    assert result == result_to_assert
    assert len(result) == paginator.boundaries


@pytest.mark.parametrize(
    "total_pages, pagination, result_to_assert",
    (
        (10, deque([-2, -1, 0, 1]), deque([1])),
        (10, deque([9, 10, 11]), deque([9, 10])),
    ),
    ids=["under_zero", "over_total_pages"],
)
def test__slice_valid_pagination(
    paginator: PaginationGenerator, total_pages, pagination, result_to_assert
):
    paginator.total_pages = total_pages

    result = paginator._slice_valid_pagination(pagination)

    assert result == result_to_assert
    assert isinstance(result, deque)


@pytest.mark.parametrize(
    "pagination, indexes_to_fill",
    (
        (deque([1, 10]), [1]),
        (deque([1, 5, 6, 10]), [3, 1]),
    ),
    ids=[
        "one_interval",
        "two_interval",
    ],
)
def test__get_indexes_to_fill_with_ellipsis(
    paginator: PaginationGenerator, pagination, indexes_to_fill
):
    paginator.total_pages = 10
    result = paginator._get_indexes_to_fill_with_ellipsis(pagination)

    assert list(result) == indexes_to_fill


@pytest.mark.parametrize(
    "pagination, index_to_assert",
    (
        (deque([1, 2, 3]), 0),
        (deque([6, 10]), 0),
    ),
    ids=[
        "find_first_page_one",
        "deduce_first_page",
    ],
)
def test__find_first_valid_number_index(
    paginator: PaginationGenerator, pagination, index_to_assert
):
    result = paginator._find_first_valid_number_index(pagination)

    assert result == index_to_assert


@pytest.mark.parametrize(
    "pagination, index_to_assert",
    (
        (deque([1, 2, 3]), 2),
        (deque([6, 10]), 3),
    ),
    ids=[
        "find_first_page_one",
        "deduce_first_page",
    ],
)
def test__find_last_valid_number_index(
    paginator: PaginationGenerator, pagination, index_to_assert
):
    paginator.total_pages = 3
    result = paginator._find_last_valid_number_index(pagination)

    assert result == index_to_assert


@pytest.mark.parametrize(
    "pagination, next_chunk, result_to_assert",
    (
        (deque([1, 2, 3]), deque([3]), deque([1, 2])),
        (deque([1, 2, 3]), deque([]), deque([1, 2, 3])),
        (deque([]), deque([3]), deque([])),
    ),
    ids=[
        "success",
        "not_next_chunk",
        "not_pagination",
    ],
)
def test__remove_overlapping_numbers(
    paginator: PaginationGenerator, pagination, next_chunk, result_to_assert
):
    result = paginator._remove_overlapping_numbers(pagination, next_chunk)

    assert result == result_to_assert


def test_build_pagination(
    mocker,
    paginator: PaginationGenerator,
):
    mocker.patch.object(PaginationGenerator, "_get_beggining", restur_value=deque([]))
    mocker.patch.object(PaginationGenerator, "_get_middle", restur_value=deque([]))
    mocker.patch.object(PaginationGenerator, "_get_end", restur_value=deque([]))
    mocker.patch.object(
        PaginationGenerator, "_remove_overlapping_numbers", restur_value=deque([])
    )
    mocker.patch.object(
        PaginationGenerator, "_slice_valid_pagination", restur_value=deque([])
    )
    mocker.patch.object(
        PaginationGenerator,
        "_get_indexes_to_fill_with_ellipsis",
        restur_value=deque([]),
    )

    assert isinstance(paginator.build_pagination(), MagicMock)
