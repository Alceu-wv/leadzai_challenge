import sys
from collections import deque
from itertools import islice
from typing import Deque, Iterable

from paginator_generator.error_handler import PaginationGeneratorErrorHandler

sys.setrecursionlimit(10**6)


class PaginationGenerator:
    FIRST_PAGE = 1
    ELLIPSIS = "..."

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

    def build_pagination(self) -> Deque:

        """
        Example
        ------
        current_page = 4; total_pages = 5; boundaries = 1; around = 0
        Expected result: [1, ..., 4, 5]
        """

        beggining = self._get_beggining()
        middle = self._get_middle()
        end = self._get_end()

        pagination = beggining
        self._remove_overlapping_numbers(pagination, middle)
        pagination += middle
        self._remove_overlapping_numbers(pagination, end)
        pagination += end

        pagination = self._slice_valid_pagination(pagination)

        indexes_to_fill_with_ellipsis = self._get_indexes_to_fill_with_ellipsis(
            pagination
        )

        for index in indexes_to_fill_with_ellipsis:
            pagination.insert(index, self.ELLIPSIS)

        return pagination

    def _get_beggining(self) -> Deque:
        """Get first chunk of pagination"""

        return deque(range(self.FIRST_PAGE, self.FIRST_PAGE + self.boundaries))

    def _get_middle(self) -> Deque:
        """Get middle chunk of pagination"""

        middle = deque([self.current_page])
        for i in range(1, self.around + 1):
            middle.append(self.current_page + i)
            middle.appendleft(self.current_page - i)

        return self._slice_valid_pagination(middle)

    def _get_end(self) -> Deque:
        """Get final chunk of pagination"""
        context_total_pages = self.total_pages + 1
        return deque(range(context_total_pages - self.boundaries, context_total_pages))

    def _slice_valid_pagination(self, pagination: Deque) -> Deque:
        """Remove less or equal zero numbers and numbers greater than last page"""

        if not pagination:
            return pagination
        first_valid_number_index = self._find_first_valid_number_index(pagination)
        last_valid_number_index = self._find_last_valid_number_index(pagination)
        return deque(
            islice(pagination, first_valid_number_index, last_valid_number_index + 1)
        )

    def _get_indexes_to_fill_with_ellipsis(self, pagination: Deque) -> Iterable:
        """Find indexes where ellipsis signal should be putted"""

        indexes_to_fill = []

        if not pagination or pagination == deque([0]):
            return indexes_to_fill

        if pagination[0] != self.FIRST_PAGE:
            indexes_to_fill.append(0)

        for count, value in enumerate(pagination):
            try:
                if value + 1 != pagination[count + 1]:
                    indexes_to_fill.append(count + 1)
            except IndexError:
                break

        if pagination[-1] != self.total_pages:
            indexes_to_fill.append(len(pagination))

        return reversed(indexes_to_fill)

    def _find_first_valid_number_index(self, numbers: Deque) -> Deque:
        try:
            return numbers.index(self.FIRST_PAGE)
        except ValueError:
            return 0

    def _find_last_valid_number_index(self, numbers: Deque) -> Deque:
        try:
            return numbers.index(self.total_pages)
        except ValueError:
            return self.total_pages

    def _remove_overlapping_numbers(
        self, pagination: Deque, next_chunk: Deque
    ) -> Deque:
        """Remove numbers from pagination that would be overlaped by next chunk append"""

        if not pagination or not next_chunk:
            return pagination
        
        last_unique_number = pagination[-1]
        if last_unique_number >= next_chunk[0]:
            pagination.pop()
            return self._remove_overlapping_numbers(pagination, next_chunk)
        else:
            return deque(
                islice(pagination, 0, pagination.index(last_unique_number) + 1)
            )
