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

Copy settings.py.example to settings.py and edit it to match your login /
password (or leave it empty, most articles are available freely anyway).

Put the provided jw2html.sh into your $PATH and edit it to
match the path to the jw2html/ source directory.

Then you can download the current issue as found under
http://jungle-world.com/inhalt/ :

$ jwhtml.sh

If you want to download a specific issue, use this:

$ jw2html.sh 2012/46



For more technical uses, you can import the python class or run
it like this:

$ python jw2html/__init__.py

It will create a cache dir of downloaded stories as sepcified in settings.py
and create a cover image and an HTML file to feed to your favourite epub
converter in your current directory.
