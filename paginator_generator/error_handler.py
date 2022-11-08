class PaginationGeneratorError(ValueError):
    ...


class PaginationGeneratorErrorHandler:
    FIRST_PAGE = 1

    """
    PaginationGenerator helper class to handle input corner cases.
    """

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        self.current_page = current_page
        self.total_pages = total_pages
        self.boundaries = boundaries
        self.around = around

    def _check_current_page_out_of_range(self):
        if self.current_page > (self.total_pages) or self.current_page < (
            self.FIRST_PAGE
        ):
            raise PaginationGeneratorError(
                "'current_page' must be within the range of 'total_pages'."
            )

    def check_for_input_errors(self):
        self._check_current_page_out_of_range()
