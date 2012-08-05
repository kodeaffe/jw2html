#!/usr/bin/env python
# vim: set fileencoding=utf-8
"""Jungle World 2 HTML

Download the current issue and prepare for conversion to epub.

"""
__docformat__ = "epytext en"
import sys, os, getopt, urllib, urllib2, re, json, time, logging
from BeautifulSoup import BeautifulSoup

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)



class JW2HTML (object):
	"""Download an issue of Jungle World + prepare for conversion to epub."""
	def __init__ (self, user, password, server, cachedir):
		self.user = user
		self.password = password
		self.url_server = server

		self.cachedir = cachedir
		if not os.path.exists(self.cachedir):
			os.mkdir(self.cachedir)

		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, self.url_server, self.user, self.password)
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
		@return: fetched HTML
		@rtype: str
		"""
		if is_index:
			filename = os.path.join(self.cachedir, 'index.html')
		else:
			basename = os.path.basename(uri)
			filename = os.path.join(self.cachedir, basename)

		# always fetch index from url
		if not is_index and os.path.exists(filename):
			LOGGER.info('Retrieving from file %s...' % filename)
			with open(filename, 'r') as f:
				html = f.read()
		else:
			url = self.url_server + uri
			LOGGER.info('Retrieving from url %s...' % url)
			html = urllib2.urlopen(url).read()
			with open(filename, 'w') as f:
				f.write(html)

		return html


	def get_meta (self, soup):
		"""Get meta data out of given soup.

		@param soup: soup which contains the meta data
		@type soup: BeautifulSoup
		@return: meta data
		@rtype: { 'title': str, 'issue_no': str, 'uri_cover': str }
		"""
		div = soup.find('div', attrs={'class':'cover_thumb'})
		title = div.find('p').text

		# title == u'Jungle World Nr. 31/12,2. August 2012'
		issue_no = title.split('.')[1:2][0].split(',')[0].strip()

		uri_cover = dict(div.find('img').attrs)['src'].replace('thumb_', '')

		LOGGER.info('META info: title %s, issue_no %s, uri_cover %s' % (
			title, issue_no, uri_cover))
		return {
			'title': title,
			'issue_no': issue_no,
			'uri_cover': uri_cover
		}


	def get_indexsoup (self):
		"""Get soup of index page.

		@return: soup of index page
		@rtype: BeautifulSoup
		"""
		index = self._fetch_html('/inhalt/', True)
		return BeautifulSoup(index,
			convertEntities=BeautifulSoup.HTML_ENTITIES)


	def get_story (self, uri):
		"""Get one story / article from given uri.

		@param uri: URI of story
		@type uri: str
		@return: story
		@rtype: str
		"""
		page = self._fetch_html(uri)
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
				stories[uri] = self.get_story(uri)

		return stories


	def build_html (self, meta, stories):
		"""Build output HTML document.

		Also writes to file.

		@param meta: meta data
		@type meta: as returned by get_meta
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
''' % (meta['title'])]

		for story in stories.itervalues():
			html.append(story + '\n')

		html.append('</body></html>')

		filename = 'JW-' + meta['issue_no'].replace('/', '.') + '.html'
		with open(filename, 'w') as f:
			# yet again UnicodeEncodeError f.write(''.join(html))
			for line in html:
				f.write(line + '\n')
		return html


	def download_cover (self, uri):
		"""Download the cover image.

		@param uri: uri to download from
		@type uri: str
		"""
		filename = os.path.basename(uri)
		LOGGER.info('Downloading cover image...')
		urllib.urlretrieve(self.url_server + uri, filename)


	def run (self):
		"""Run this method when using this class."""
		index = self.get_indexsoup()
		meta = self.get_meta(index)
		stories = self.get_stories(index)

		self.build_html(meta, stories)
		self.download_cover(meta['uri_cover'])
