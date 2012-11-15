#!/usr/bin/env python
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
__docformat__ = "epytext en"
import sys, os, getopt, urllib, urllib2, httplib, re, json, time, logging, shutil, random, string
from BeautifulSoup import BeautifulSoup

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)



class JW2HTML (object):
    """Download an issue of Jungle World + prepare for conversion to epub."""
    def __init__ (self, user, password, server, uri_index, cache_dir):
        self.user = user
        self.password = password
        self.server = server
        self.uri_index = uri_index

        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.title = 'Unknown issue of Jungle World'
        self.uri_cover = ''
        self.issue_no = ''.join(random.sample(string.letters + string.digits, 8))
        self.issue_dir = os.path.join(self.cache_dir, self.issue_no)

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self.server, self.user, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)


    def _fetch_html (self, uri, is_index=False):
        """Retrieve HTML from either an existing cache dir or the internet.

        The index page is always fetched from the internet.

        @param uri: URI to fetch
        @type uri: str
        @param is_index: if uri is the index page
        @type is_index: bool
        @return: fetched HTML or None
        @rtype: str
        """
        if is_index:
            filename = os.path.join(self.cache_dir, 'index.html')
        else:
            basename = os.path.basename(uri)
            filename = os.path.join(self.issue_dir, basename)

        # always fetch index from url
        if not is_index and os.path.exists(filename):
            LOGGER.info('Retrieving from file %s...' % filename)
            with open(filename, 'r') as f:
                html = f.read()
        else:
            url = self.server + uri
            LOGGER.info('Retrieving from url %s to file %s...' % (
                url, filename))
            try:
                html = urllib2.urlopen(url).read()
                with open(filename, 'w') as f:
                    f.write(html)
            except httplib.BadStatusLine as err:
                LOGGER.warn('Failed: %s' % err)
                return None

        return html


    def parse_index (self):
        """Parse index file.

        Populates member variables issue_no, title, and uri_cover.
        Copies index file to issue dir.
        Return index soup.

        @return: soup of the index file
        @rtype: BeautifulSoup
        """
        index = self._fetch_html(self.uri_index, True)
        soup = BeautifulSoup(index,
            convertEntities=BeautifulSoup.HTML_ENTITIES)

        div = soup.find('div', attrs={'class':'cover_thumb'})
        self.title = div.find('p').text

        # e.g. title == u'Jungle World Nr. 31/12,2. August 2012'
        issue = self.title.split('.')[1:2][0].split(',')[0].strip().split('/')
        self.issue_no = issue[1] + '.' + issue[0]
        self.issue_dir = os.path.join(self.cache_dir, self.issue_no)
        if not os.path.exists(self.issue_dir):
            os.makedirs(self.issue_dir)
        shutil.move(os.path.join(self.cache_dir, 'index.html'),
            os.path.join(self.issue_dir, 'index.html'))

        self.uri_cover = dict(div.find('img').attrs)['src'].replace('thumb_', '')

        LOGGER.info('META info: title %s, issue_no %s uri_cover %s' % (
            self.title, self.issue_no, self.uri_cover))
        return soup


    def get_story (self, uri):
        """Get one story / article from given uri.

        @param uri: URI of story
        @type uri: str
        @return: story
        @rtype: str
        """
        # possibly links to other issues
        if not uri.endswith('.html'):
            return None
        if self.issue_no.replace('.', '/') not in uri:
            return None

        page = self._fetch_html(uri)
        if not page:
            return None

        soup = BeautifulSoup(page,
            convertEntities=BeautifulSoup.HTML_ENTITIES)
        story = soup.find('div', attrs={'class':'story'})
        if story:
            return str(story)
        else:
            return None


    def get_stories (self, soup):
        """Get all stories of current issue.

        @param soup: soup of index page to check for links to stories
        @type soup: BeautifulSoup
        @return: all stories of current issue.
        @rtype: { uri: str, }
        """
        regex = re.compile('/artikel')
        first = True
        stories = {}

        LOGGER.info('Getting stories...')
        for anchor in soup.findAll('a', attrs={'href':regex}):
            if first:
                first = False
                continue

            try:
                uri = dict(anchor.attrs)['href']
            except IndexError:
                continue

            if uri not in stories:
                story = self.get_story(uri)
                if story:
                    stories[uri] = story

        return stories


    def build_html (self, stories):
        """Build output HTML document.

        Also writes to file.

        @param stories: stories of this issue
        @type stories: as returned by get_stories
        @return: resulting HTML document
        @rtype: str
        """
        LOGGER.info('Building HTML...')
        html = ['''<!DOCTYPE html>
<html>
<head>
    <title>%s</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="author" content="Redaktion Jungle World" />
    <meta name="description" content="Jungle World. Die linke Wochenzeitung aus Berlin." />
</head>
<body>
''' % (self.title)]

        for story in stories.itervalues():
            html.append(story + '\n')

        html.append('</body></html>')

        filename = os.path.join(
            self.issue_dir, 'JW-' + self.issue_no + '.html')
        with open(filename, 'w') as f:
            # yet again UnicodeEncodeError f.write(''.join(html))
            for line in html:
                f.write(line + '\n')
        return html


    def download_cover (self):
        """Download the cover image."""
        filename = os.path.join(self.issue_dir,
            os.path.basename(self.uri_cover))
        LOGGER.info('Downloading cover image...')
        urllib.urlretrieve(self.server + self.uri_cover, filename)


    def run (self):
        """Run this method when using this class."""
        index = self.parse_index()
        stories = self.get_stories(index)

        self.build_html(stories)
        self.download_cover()
