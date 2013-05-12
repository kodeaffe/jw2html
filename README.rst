README
======

Alas, there is no epub version of the Jungle World, http://jungle-world.com .

Hence this little module to download the current issue and pack it into one
HTML file which can then be converted to epub (using e.g. http://calibre-ebook.com).
It also downloads the cover image for easy inclusion when creating the book
in calibre.

INSTALL
=======

Python Package Index (http://pypi.python.org)
---------------------------------------------

$ pip3 install jw2html


Source (http://github.com/marmorkuchen/jw2html)
-----------------------------------------------
Install dependencies:

$ apt-get install python3-bs4

OR

$ pip3 install beautifulsoup4

Create source distribution and install that:

$ python3 setup.py sdist

$ cd dist/ && tar xzf JW2HTML-$VERSION && cd JW2HTML-$VERSION

$ sudo python3 setup.py install



Usage
=====

Copy /etc/jw2html.ini to $HOME/.jw2html.ini and edit it to match your login / password. Or don't bother to copy and edit, because most articles are available freely anyway.

Setuptools should have installed a script jw2html to run the package for you. Then you can download the current issue as found under http://jungle-world.com/inhalt/ just by typing:

$ jw2html

If you want to download a specific issue, use this:

$ jw2html 2013.13


For more technical uses you can import the package and run it like this:

$ python3 -c 'import jw2html; jw2html.main()' $*


It will create a directory of downloaded stories as a subdirectory of CACHEDIR as specified in jw2html.ini, e.g. html/2013.13/ .  It will also download a cover image and put the generated HTML file into that directory. The HTML file, e.g. html/2013.13/JW-2013.13.html, and cover image, e.g. html/2013.13/01-titel.gif, can then be fed to your favourite epub converter.
