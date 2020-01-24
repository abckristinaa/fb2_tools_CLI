import argparse
import textwrap

from db_methods import Connect


def cli_parser() -> tuple:
    """ Defines CLI and returns arguments from it. """
    parser = argparse.ArgumentParser(
        prog="seeker.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Search a book by author, book title and year.
        Search is case sensitive and find only full match."""),
        epilog=textwrap.dedent("""
        EXAMPLE OF USAGE:
            seeker.py -a 'Андрей Жвалевский'
            seeker.py -a 'Андрей Жвалевский' -n 'Мастер силы'
            seeker.py -y 2007
            """))
    parser.add_argument("-a", dest="author", help="search by author")
    parser.add_argument("-n", dest="book_name", help="search by book title")
    parser.add_argument("-y", dest="year", help="search by year")
    parser.add_argument("-s", dest="s_flag", action="store_true",
                        help="show only book number")
    parser.add_argument(
        "-ver",
        dest="version",
        action="store_const",
        const="1.0 build 22-01-2020",
        help="show version")
    args = parser.parse_args()
    return args.author, args.book_name, args.year, args.s_flag, args.version


def pretty_print(result: list) -> None:
    """ Prints search results in readable format. """
    len_author = max([len(str(item[1])) for item in result if item[1]])
    len_num = max([len(str(item[0])) for item in result if item[0]])
    fill = " "
    print("Search results:")
    print(
        "ID".center(len_num, fill),
        "Author".center(len_author, fill),
        "Year".center(10, fill),
        "Title",
        sep=" | ",
    )
    print("-" * 80)
    for num, author, book, year in result:
        print(
            str(num).rjust(len_num, fill),
            author.ljust(len_author, fill),
            year.ljust(10, fill),
            book,
            sep=" | ",
        )


def run(author: str, bookname: str, year: str, s_flag: bool, version: str):
    """ Defines the order of execution the program."""
    if not author and not bookname and not year:
        print("Try to use help for running: seeker.py -h")
    elif version:
        print(f"version {version}")
    else:
        year = str(year) if year else None
        result = Connect().find_book((author, bookname, year))
        if not result:
            print("No result found.")
        else:
            if not s_flag:
                pretty_print(result)
            else:
                print("Following numbers found:")
                for item in result:
                    print(item[0])


if __name__ == "__main__":
    author, book_name, year, s_flag, version = cli_parser()
    run(author, book_name, year, s_flag, version)
