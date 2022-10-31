from paginator_generator.error_handler import PaginationGeneratorError
from paginator_generator.generator import PaginationGenerator


def input_integer(message: str) -> int:
    """Receive an argument from command line, repeat message until the argument can be parsed to integer"""

    argument = None
    while argument is None or argument < 0:
        try:
            argument = int(input(message))
            if argument < 0:
                raise ValueError
        except ValueError:
            print("Input must be a positive number.")
    return argument


def run():

    total_pages = input_integer("Insert total pages: ")
    current_page = input_integer("Insert current page: ")
    boundaries = input_integer("Insert boundaries: ")
    around = input_integer("Insert around: ")

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
