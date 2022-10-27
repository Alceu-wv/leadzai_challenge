import pytest

from paginator_generator.generator import PaginationGenerator

@pytest.mark.parametrize(
    "boundaries, result_to_assert",
    (
        (1, {1}),
        (2, {1, 2}),
        (3, {1, 2, 3}),
    )
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
    )
)
def test__get_middle(paginator: PaginationGenerator, current_page, around, result_to_assert):
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
    )
)
def test__get_end(paginator: PaginationGenerator, pages, boundaries, result_to_assert):
    paginator.boundaries = boundaries
    paginator.last_page = pages
    
    result = paginator._get_end()
    
    assert isinstance(result, set)
    assert result == result_to_assert
    assert len(result) == paginator.boundaries

def test__clean_numbers_out_of_range():
    pass

def test__get_indexes_to_be_fold():
    pass

def test_build_pagination():
    pass