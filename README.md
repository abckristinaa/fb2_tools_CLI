# fb2_tools_CLI

A bunch of command line utilities for working with local fb2 books library.


# Installation

Pull the latest version of the image from the docker.
```
docker pull abckristinaa/fb2_tool:latest
```

# How to use from command line

`digger.py:`

```
usage: digger.py [-h] [-s DIR_PATH | -a BOOK_PATH] [-u] [-v] [-ver]

Adds a book from BOOK_PATH to a FB2 library database. The library  
database is creating from DIR_PATH. Supports fb2, fb2.zip, fb2.gz.

optional arguments:
  -h, --help       show this help message and exit
  -s DIR_PATH      the full path to a directory containing books
  -a BOOK_PATH     the full path to a book
  -u, --update     update the book info
  -v, --verbose    show additional information about execution
  -ver, --version  show version

Note, that if flag -u is not given, the information about the book 
will not be updated. 
```

`seeker.py:`
```
usage: seeker.py [-h] [-a AUTHOR] [-n BOOK_NAME] [-y YEAR] [-s] [-ver]

Search a book by author, book title and year.
Search is case sensitive and find only full match.

optional arguments:
  -h, --help    show this help message and exit
  -a AUTHOR     search by author
  -n BOOK_NAME  search by book title
  -y YEAR       search by year
  -s            show only book number
  -ver          show version

EXAMPLE OF USAGE:
    seeker.py -a 'Андрей Жвалевский'
    seeker.py -a 'Андрей Жвалевский' -n 'Мастер силы'
    seeker.py -y 2007
```

`wiper.py`

```
usage: wiper.py [-h] [-n NUMBER | -a] [-ver]

Remove a book from the FB2 library database by it's ID. 

optional arguments:

  -h, --help       show this help message and exit
  -n NUMBER        delete a book by number
  -a, --all        remove all from the library
  -ver, --version  show version```
