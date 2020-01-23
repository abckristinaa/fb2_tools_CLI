import argparse
import gzip
import os
import textwrap
import time
import zipfile
from xml.etree import ElementTree as ElT

from db_methods import Connect

TAGS = ("first-name", "last-name", "book-title", "date")
EXTENSIONS = (".fb2", ".fb2.zip", ".fb2.gz")


def cli_parser() -> tuple:
    """ Defines CLI and returns arguments from it. """
    parser = argparse.ArgumentParser(
        prog="digger.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
        Adds a book from BOOK_PATH to a FB2 library database. The library  
        database is creating from DIR_PATH. Supports fb2, fb2.zip, fb2.gz.
        """
        ),
        epilog=textwrap.dedent(
            """
        Note, that if flag -u is not given, the information about the book 
        will not be updated. """
        ),
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s",
        dest="dir_path",
        help="the full path to a directory containing books",
    )
    group.add_argument(
        "-a", dest="book_path", help="the full path to a book",
    )
    parser.add_argument(
        "-u",
        "--update",
        dest="u_flag",
        action="store_true",
        help="update the book info",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="show additional information about execution",
    )
    parser.add_argument(
        "-ver",
        "--version",
        dest="version",
        action="store_const",
        const="1.0 build 22-01-2020",
        help="show version",
    )
    args = parser.parse_args()
    return (
        args.dir_path,
        args.book_path,
        args.u_flag,
        args.verbose,
        args.version,
    )


class Digger:
    @staticmethod
    def paths_is_valid(dir_path: str, book_path: str) -> bool:
        """Returns True if given paths are exists. """
        paths_to_check = [i for i in (dir_path, book_path) if i]
        return all(os.path.exists(i) for i in paths_to_check)

    @staticmethod
    def scan_folders(dir_path: str) -> str:
        """ Recursively walks the dir_path. Returns filepath if fb2. """
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(EXTENSIONS):
                    name = os.path.join(root, file)
                    yield name
        else:
            print("The scan is complete.")

    @staticmethod
    def process_extension(file_ext: str) -> tuple:
        """ Returns filepath or file stream depending on file extension. """
        if file_ext.lower().endswith(".fb2"):
            return file_ext, False
        elif file_ext.lower().endswith(".fb2.gz"):
            try:
                gz = gzip.open(file_ext)
                return gz, gz
            except gzip.BadGzipFile:
                print(f"Bad gzip file {file_ext}")
        else:
            zipped = zipfile.ZipFile(file_ext)
            try:
                for name in zipped.namelist():
                    return zipped.open(name), zipped
            except zipfile.BadZipFile:
                print(f"Bad zip file {file_ext}")
                zipped.close()

    @staticmethod
    def read_tags(file_: str, name: str, verbose: bool) -> tuple:
        """ Returns a tuple with selected data from book tags. """
        data = {key: None for key in TAGS}
        try:
            for num, elem in enumerate(ElT.iterparse(file_)):
                tag = elem[1].tag.split("}")[-1]
                if num < 20:
                    if tag in TAGS:
                        data[tag] = (
                            elem[1].text if not data[tag] else data[tag]
                        )
                else:
                    author = [
                        data[i] for i in ("first-name", "last-name") if data[i]
                    ]
                    data["author"] = " ".join(author) if author else None
                    if not data["book-title"]:
                        data["book-title"] = name.split("/")[-1]
                    return tuple(
                        data[i] for i in ("author", "book-title", "date")
                    )
        except ElT.ParseError:
            if verbose:
                print(file_, " can't read")
            else:
                pass

    @classmethod
    def prepare_data(cls, f_path: str, verbose: bool) -> tuple:
        """Process all files and returns a tuple with readed tags"""
        filepath, zipped = cls.process_extension(f_path)
        if filepath:
            data = cls.read_tags(filepath, f_path, verbose)
            if zipped:
                zipped.close()
            return data

    @classmethod
    def run(
        cls,
        dirpath: str,
        bookpath: str,
        uflag: bool,
        verbose: bool,
        version: str,
    ) -> None:
        """ Defines main flow of execution. """
        if not dirpath and not bookpath and not version:
            print("Try to use help for running: digger.py -h")
        elif version:
            print(f"version {version}")
        else:
            if not cls.paths_is_valid(dirpath, bookpath):
                raise ValueError(f"Wrong path is given.")

        conn = Connect()
        if dirpath:
            data_for_db = []
            if verbose:
                print("Start scanning...")
                counter = 0
            for f_path in cls.scan_folders(dirpath):
                data = cls.prepare_data(f_path, verbose)
                if len(data_for_db) < 1000:
                    data_for_db.append(data) if data else ""
                else:
                    if verbose:
                        counter += len(data_for_db)
                        print(f"{counter} books readed...")
                    conn.insert(data_for_db)
                    data_for_db = []
            if data_for_db:
                if verbose:
                    counter += len(data_for_db)
                    print(f"{counter} books readed total.")
                conn.insert(data_for_db)

        if bookpath:
            data = cls.prepare_data(bookpath, verbose)
            found = conn.find_book(data)
            if found:
                if uflag:
                    for item in found:
                        conn.update_book_info(item)
            else:
                conn.insert(data)
                print("The book is added.")


if __name__ == "__main__":
    start = time.time()
    dir_path, book_path, u_flag, verbose, version = cli_parser()
    Digger().run(dir_path, book_path, u_flag, verbose, version)
    print(f"Time elapsed: {int(time.time() - start)} secs" if verbose else "")
