from typing import Iterable

from paginator_generator.error_handler import PaginationGeneratorErrorHandler


class PaginationGenerator:
    FIRST_PAGE = 1

    """
    Generate custom pagination to show in a footer website.
    """

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        """
        Parameters
        ----------
        current_page : int
            Page being currently displayed
        total_pages : int
            All existent pages
        boundaries : int
            how many pages we want to link in the beginning, or end (meaning, how many
            pages starting at page 1 and how many leading up to the last page, inclusive)
        around : int
            how many pages we want to link before and after the current page, exclusive.
            For pages with no direct link we should use one set of three points (...) per set of pages hidden.

        Raises
        ------
        PaginationGeneratorError
            If parameter inputs violetes calculation logic.
        """

        self.current_page = current_page
        self.total_pages = total_pages
        self.boundaries = boundaries
        self.around = around

        PaginationGeneratorErrorHandler(
            current_page, total_pages, boundaries, around
        ).check_for_input_errors()

    def build_pagination(self) -> list:

        """
        Example
        ------
        current_page = 4; total_pages = 5; boundaries = 1; around = 0
        Expected result: [1, ..., 4, 5]
        """

        begining = self._get_beggining()
        midle = self._get_middle()
        end = self._get_end()

        builded_pagination = sorted(list(begining | end | midle | {self.current_page}))
        builded_pagination = self._clean_numbers_out_of_range(builded_pagination)

        get_indexes_to_be_fold = self._get_indexes_to_be_fold(builded_pagination)

        for index in get_indexes_to_be_fold:
            builded_pagination.insert(index, "...")

        return builded_pagination

    def _get_indexes_to_be_fold(self, builded_pagination: list) -> Iterable:
        indexes_to_be_fold = []
        for count, value in enumerate(builded_pagination):
            try:
                if value + 1 != builded_pagination[count + 1]:
                    indexes_to_be_fold.append(count + 1)
            except IndexError:
                break
        return reversed(indexes_to_be_fold)

    def _get_beggining(self) -> set:
        return set(range(self.FIRST_PAGE, self.FIRST_PAGE + self.boundaries))

    def _get_middle(self) -> set:
        middle = set()
        for i in range(1, self.around + 1):
            middle.add(self.current_page + i)
            middle.add(self.current_page - i)

        return middle

    def _get_end(self) -> set:
        return set(range(self.total_pages, self.total_pages - self.boundaries, -1))

    def _clean_numbers_out_of_range(self, list_of_numbers: list) -> list:
        numbers = list_of_numbers.copy()
        for number in numbers:
            if number <= 0 or number > self.total_pages:
                list_of_numbers.remove(number)
        return list_of_numbers
