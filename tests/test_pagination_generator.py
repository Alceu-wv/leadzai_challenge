from unittest.mock import MagicMock

import pytest

from paginator_generator.generator import PaginationGenerator


@pytest.mark.parametrize(
    "boundaries, result_to_assert",
    (
        (1, {1}),
        (2, {1, 2}),
        (3, {1, 2, 3}),
    ),
)
def test__get_beggining(paginator: PaginationGenerator, boundaries, result_to_assert):
    paginator.boundaries = boundaries

    result = paginator._get_beggining()

    assert isinstance(result, set)
    assert result == result_to_assert
    assert len(result) == paginator.boundaries


@pytest.mark.parametrize(
    "current_page, around, result_to_assert",
    (
        (10, 1, {9, 11}),
        (10, 2, {8, 9, 12, 11}),
        (10, 3, {7, 8, 9, 11, 12, 13}),
    ),
)
def test__get_middle(
    paginator: PaginationGenerator, current_page, around, result_to_assert
):
    paginator.around = around
    paginator.current_page = current_page

    result = paginator._get_middle()

    assert isinstance(result, set)
    assert result == result_to_assert
    assert len(result) == around * 2


@pytest.mark.parametrize(
    "pages, boundaries, result_to_assert",
    (
        (10, 1, {10}),
        (10, 2, {9, 10}),
        (10, 3, {8, 9, 10}),
    ),
)
def test__get_end(paginator: PaginationGenerator, pages, boundaries, result_to_assert):
    paginator.boundaries = boundaries
    paginator.total_pages = pages

    result = paginator._get_end()

    assert isinstance(result, set)
    assert result == result_to_assert
    assert len(result) == paginator.boundaries


@pytest.mark.parametrize(
    "total_pages, list_to_clean, result_to_assert",
    (
        (10, [-2, -1, 0, 1], [1]),
        (10, [9, 10, 11], [9, 10]),
    ),
    ids=["under_zero", "over_total_pages"],
)
def test__clean_numbers_out_of_range(
    paginator: PaginationGenerator, total_pages, list_to_clean, result_to_assert
):
    paginator.total_pages = total_pages

    result = paginator._clean_numbers_out_of_range(list_to_clean)

    assert result == result_to_assert
    assert isinstance(result, list)


@pytest.mark.parametrize(
    "list_to_parse, indexes_to_be_fold",
    (
        ([0, 2], [1]),
        ([10, 20], [1]),
        ([10, 12, 13, 15], [3, 1]),
        ([10, 20, 30], [2, 1]),
    ),
    ids=[
        "one_interval_short",
        "one_interval_long",
        "two_interval_short",
        "two_interval_long",
    ],
)
def test__get_indexes_to_be_fold(
    paginator: PaginationGenerator, list_to_parse, indexes_to_be_fold
):
    result = paginator._get_indexes_to_be_fold(list_to_parse)

    assert list(result) == indexes_to_be_fold


def test_build_pagination(
    mocker,
    paginator: PaginationGenerator,
):
    mocker.patch.object(PaginationGenerator, "_get_beggining", restur_value=set())
    mocker.patch.object(PaginationGenerator, "_get_middle", restur_value=set())
    mocker.patch.object(PaginationGenerator, "_get_end", restur_value=set())
    mocker.patch.object(
        PaginationGenerator, "_clean_numbers_out_of_range", restur_value=set()
    )
    mocker.patch.object(
        PaginationGenerator, "_get_indexes_to_be_fold", restur_value=set()
    )

    assert isinstance(paginator.build_pagination(), MagicMock)
