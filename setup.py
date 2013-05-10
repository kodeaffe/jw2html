import os
from setuptools import setup, find_packages
from jw2html import VERSION


setup(
    name='JW2HTML',
    version=VERSION,
    description='JW2HTML converts an issue of the Jungle World from the website to a single HTML file to be used for epub conversion by e.g. calibre.',
    long_description='Alas, there is no epub version of the Jungle World, http://jungle-world.com . Hence this little module to download the current issue and pack it into one HTML file which can then be converted to epub (using e.g.  http://calibre-ebook.com). It also downloads the cover image for easy inclusion when creating the book in calibre.',
    license='GPL',
    keywords='jungle world newspaper html epub convert',
    url='https://github.com/marmorkuchen/jw2html',
    author='marmorkuchen',
    author_email='marmorkuchen@kodeaffe.de',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('doc', ['README.rst', 'LICENSE']),
        (os.path.join(os.sep, 'etc'), ['jw2html.ini',]),
    ],
    entry_points={
        'console_scripts': [
            'jw2html = jw2html:main',
        ]
    },
    install_requires=[
        'beautifulsoup4',
    ],
)
