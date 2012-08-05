README
======

Alas, there is no epub version of the Jungle World, http://jungle-world.com .

Hence this little module to download the current issue and pack it into one
HTML file which can then be converted to epub (using e.g. http://calibre-ebook.com).
It also downloads the cover image for easy inclusion when creating the book
in calibre.



Dependencies
============

$ apt-get install python-beautifulsoup

OR

$ pip install BeautifulSoup



Usage
=====

Edit settings.py to for your login / password (or leave it empty, most
articles are available freely anyway)

Import the class wherever you want or run it like this:

$ python jw2html/__init__.py


It will create a cache dir of downloaded stories, a cover image and an HTML
file to feed to your favourite epub converter.
