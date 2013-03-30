README
======

Alas, there is no epub version of the Jungle World, http://jungle-world.com .

Hence this little module to download the current issue and pack it into one
HTML file which can then be converted to epub (using e.g. http://calibre-ebook.com).
It also downloads the cover image for easy inclusion when creating the book
in calibre.



Dependencies
============

$ apt-get install python3-bs4

OR

$ pip install beautifulsoup4



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

$ jw2html.sh 2013.13

Or for more technical uses, you can import the package and run it like this:

$ python3 -c 'import jw2html; jw2html.main()' $*

It will create a directory of downloaded stories as a subdirectory of CACHEDIR
as specified in settings.py, e.g. html/2013.13/ .
It will also download a cover image and put the generated HTML file into that
directory. The HTML file, e.g. html/2013.13/JW-2013.13.html, and cover image, e.g.
html/2013.13/01-titel.gif, can then be fed to your favourite epub converter.
