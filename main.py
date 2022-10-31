from paginator_generator.error_handler import PaginationGeneratorError
from paginator_generator.generator import PaginationGenerator


def input_argument(message: str) -> int:
    """Receive an argument from command line, repeat message until the argument can be parsed to integer"""

    argument = None
    while argument is None:
        try:
            argument = int(input(message))
        except ValueError:
            print("Input must be a number.")
    return argument


def run():

    total_pages = input_argument("Insert total pages: ")
    current_page = input_argument("Insert current page: ")
    boundaries = input_argument("Insert boundaries: ")
    around = input_argument("Insert around: ")

    try:
        result = PaginationGenerator(
            current_page, total_pages, boundaries, around
        ).build_pagination()

        print(" ".join([str(x) for x in result]))

    except PaginationGeneratorError as error:
        print(error)
        print("Try again:")
        run()


if __name__ == "__main__":
    run()
