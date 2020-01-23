import argparse
import textwrap

from db_methods import Connect


def cli_parser() -> tuple:
    """ Defines CLI and returns arguments from it. """
    parser = argparse.ArgumentParser(
        prog="wiper.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Remove a book from the FB2 library database by it's ID. Supports fb2, 
        fb2.zip, fb2.gz book extentions."""),
        allow_abbrev=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", dest="number", help="delete a book by number")
    group.add_argument(
        "-a",
        "--all",
        dest="a_flag",
        action="store_true",
        help="remove all from the library")
    parser.add_argument(
        "-ver",
        "--version",
        dest="version",
        action="store_const",
        const="1.0 build 22-01-2020",
        help="show version")
    args = parser.parse_args()
    return args.number, args.a_flag, args.version


def main(number: int, a_flag: bool, version: str) -> None:
    """Defines flow of execution for deletion from db using arguments"""
    if not number and not a_flag and not version:
        print("Try to use help for running: wiper.py -h")
    elif version:
        print(f"version {version}")
    elif a_flag:
        Connect().delete_(number, a_flag)
    else:
        conn = Connect()
        found = conn.find_by_rowid(number)
        if found:
            conn.delete_(number, a_flag, found)
        else:
            print(f"A book with number {number} not found.")


if __name__ == "__main__":
    number, a_flag, version = cli_parser()
    main(number, a_flag, version)
