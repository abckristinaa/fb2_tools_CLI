import os
import sqlite3
from configparser import ConfigParser, NoSectionError


COLUMNS = ("author", "booktitle", "date")


class Connect:
    """A class to provide methods for working with library database. """
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(self.CONFIG_PATH)
        try:
            self.conn = sqlite3.connect(self.config.get('main', 'db_name'))
        except NoSectionError:
            self.conn = sqlite3.connect("lib.db")
        self.conn.execute('PRAGMA journal_mode = off')
        sql = f"CREATE TABLE IF NOT EXISTS library({', '.join(COLUMNS)}, " \
              f"PRIMARY KEY(author, booktitle) )"
        self.conn.execute(sql)

    def insert(self, data: [list, tuple]) -> None:
        """Adds a new entry to the database."""
        cur = self.conn.cursor()
        sql = "INSERT OR IGNORE INTO library values (?, ?, ?)"
        cur.executemany(sql, data)
        self.conn.commit()
        cur.close()

    def find_book(self, book: tuple) -> list:
        """ Returns the book found by given args with it's rowid."""
        cur = self.conn.cursor()
        merge = dict(zip(COLUMNS, book))
        params = tuple(i for i in book if i)
        where = " AND ".join([f"{k} = ?" for k, v in merge.items() if v])
        sql = f"SELECT rowid, * FROM library WHERE {where}"
        cur.execute(sql, params)
        row = cur.fetchall()
        cur.close()
        return row

    def find_by_rowid(self, number: int) -> tuple:
        """ Returns the book found by author and title with it's rowid."""
        cur = self.conn.cursor()
        sql = 'SELECT rowid, * FROM library WHERE rowid = ?'
        cur.execute(sql, (number,))
        row = cur.fetchone()
        cur.close()
        return row

    def update_book_info(self, book: tuple) -> None:
        """ Updates the book info by rowid."""
        cur = self.conn.cursor()
        cols = ", ".join([f'{i} = ?' for i in COLUMNS[::-1]])
        sql = f"UPDATE library SET {cols} WHERE rowid = ?"
        cur.execute(sql, tuple(reversed(book)))
        self.conn.commit()
        print("The book info was sucessfully updated.")
        cur.close()

    def delete_(self, number, all_flag: bool, found=None):
        """ Deletes a book from database by rowid or remove all if all_flag."""
        cur = self.conn.cursor()
        if all_flag:
            sql = "DELETE from library"
            cur.execute(sql)
            print("The database sucessfully cleared.")
        else:
            sql = "DELETE from library WHERE rowid = ?"
            cur.execute(sql, (number,))
            print(f"<<{found[2]}>> removed from the database.")
        self.conn.commit()
        self.conn.close()
