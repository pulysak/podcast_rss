from django.contrib.gis.feeds import Feed
from django.utils.feedgenerator import Rss201rev2Feed, rfc2822_date
from django.utils.xmlutils import SimplerXMLGenerator

from show.models import Show, Episode


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
        handler.addQuickElement('itunes:category', attrs={'text':  category})

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


class ShowFeed(Feed):

    feed_type = AppleFeed

    def feed_copyright(self, obj):
        return obj.copyright

    def link(self, obj):
        return obj.website

    def author_email(self, obj):
        return obj.author.email

    def author_name(self, obj):
        return obj.author.name

    def get_object(self, request, *args, **kwargs):
        return (
            Show
            .objects
            .filter(id=kwargs.get('show_id'))
            .select_related('author')
            .prefetch_related('episodes')
            .first()
        )

    def description(self, obj):
        return obj.long_description

    def title(self, obj):
        return obj.name

    def items(self, obj):
        return obj.episodes.all()

    def item_enclosure_url(self, item):
        return item.file_url

    def item_enclosure_length(self, item):
        return item.file_length

    def item_enclosure_mime_type(self, item):
        return item.file_type

    def item_guid(self, item):
        return str(item.id)

    def item_pubdate(self, item):
        return item.publication_date

    def item_description(self, item):
        return item.notes

    def item_link(self, item):
        return item.link

    def feed_extra_kwargs(self, obj):
        kwargs = super().feed_extra_kwargs(obj)
        kwargs['explicit'] = obj.is_include_explicit_language
        kwargs['image'] = obj.image
        kwargs['category'] = obj.category
        kwargs['subcategory'] = obj.subcategory
        kwargs['block'] = obj.is_blocked
        kwargs['complete'] = obj.is_complete
        kwargs['type'] = Show.Type(obj.type).value
        return kwargs

    def item_extra_kwargs(self, item):
        kwargs = super().item_extra_kwargs(item)
        kwargs['duration'] = str(item.duration) if item.duration else ''
        kwargs['image'] = item.image
        kwargs['explicit'] = item.is_include_explicit_language
        kwargs['type'] = Episode.EpisodeType(item.type).value
        kwargs['season'] = str(item.season_number) if item.season_number else ''
        kwargs['episode'] = str(item.episode_number) if item.episode_number else ''
        kwargs['block'] = item.is_blocked
        kwargs['website'] = item.link
        print(kwargs)
        return kwargs
