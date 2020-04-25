from django.utils.feedgenerator import Rss201rev2Feed, rfc2822_date
from django.utils.xmlutils import SimplerXMLGenerator


class SXG(SimplerXMLGenerator):
    def addQuickElementCDATA(self, name, contents=None, attrs=None):
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self._write(f'<![CDATA[{contents}]]>')
        self.endElement(name)


class AppleFeed(Rss201rev2Feed):
    def write(self, outfile, encoding):
        handler = SXG(outfile, encoding)
        handler.startDocument()
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")

    def _add_categories(self, handler):
        category = self.feed['category']
        subcategory = self.feed['subcategory']
        if subcategory:
            handler.startElement('itunes:category', attrs={'text': category})
            handler.addQuickElement('itunes:category', attrs={'text': subcategory})
            handler.endElement('itunes:category')
            return
        handler.addQuickElement('itunes:category', attrs={'text': category})

    def _add_owner(self, handler):
        handler.startElement('itunes:owner', attrs={})
        handler.addQuickElement('itunes:name', contents=self.feed['author_name'])
        handler.addQuickElement('itunes:email', contents=self.feed['author_email'])
        handler.endElement('itunes:owner')

    def rss_attributes(self):
        return {
            'version': self._version,
            'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        }

    def add_root_elements(self, handler):
        # required
        handler.addQuickElement('title', self.feed['title'])
        handler.addQuickElementCDATA('description', self.feed['description'])
        if self.feed['language'] is not None:
            handler.addQuickElement('language', self.feed['language'])

        handler.addQuickElement('itunes:explicit', str(self.feed['explicit']).lower())
        handler.addQuickElement('itunes:image', self.feed['image'])
        self._add_categories(handler)

        # Recommended
        handler.addQuickElement('itunes:author', self.feed['author_name'])
        handler.addQuickElement('link', self.feed['link'])
        self._add_owner(handler)

        # Situational tags
        handler.addQuickElement('itunes:title', self.feed['title'])
        handler.addQuickElement('itunes:type', self.feed['type'])
        if self.feed['feed_copyright'] is not None:
            handler.addQuickElement('copyright', self.feed['feed_copyright'])
        if self.feed['block']:
            handler.addQuickElement('itunes:block', 'Yes')
        if self.feed['complete']:
            handler.addQuickElement('itunes:complete', 'Yes')

    def add_item_elements(self, handler, item):
        # Required tags
        handler.addQuickElement('title', item['title'])
        # Enclosure.
        if item['enclosures']:
            enclosures = list(item['enclosures'])
            if len(enclosures) > 1:
                raise ValueError(
                    'RSS feed items may only have one enclosure, see '
                    'http://www.rssboard.org/rss-profile#element-channel-item-enclosure'
                )
            enclosure = enclosures[0]
            handler.addQuickElement('enclosure', '', {
                'url': enclosure.url,
                'length': enclosure.length,
                'type': enclosure.mime_type,
            })

        # Recommended tags
        handler.addQuickElement('guid', item['unique_id'])
        handler.addQuickElement('pubDate', rfc2822_date(item['pubdate']))
        handler.addQuickElementCDATA('description', item['description'])
        if item['duration']:
            handler.addQuickElement('itunes:duration', item['duration'])
        if item['website']:
            handler.addQuickElement('link', item['website'])
        if item['image']:
            handler.addQuickElement('itunes:image', item['image'])
        handler.addQuickElement('itunes:explicit', str(item['explicit']).lower())

        # Situational tags
        handler.addQuickElement('itunes:title', item['title'])
        if item['episode']:
            handler.addQuickElement('itunes:episode', item['episode'])
        if item['season']:
            handler.addQuickElement('itunes:season', item['season'])
        handler.addQuickElement('itunes:episodeType', item['type'])
        if item['block']:
            handler.addQuickElement('itunes:block', 'Yes')


class SpotifyFeed(AppleFeed):
    pass
