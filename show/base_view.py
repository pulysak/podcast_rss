import datetime

from django.contrib.gis.feeds import Feed
from django.db.models import Prefetch

from show.models import Show, Episode


class BaseFeedView(Feed):

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
            .select_related('author')
            .prefetch_related(
                Prefetch(
                    'episodes',
                    queryset=Episode.objects.filter(publication_date__lte=datetime.datetime.now()),
                )
            )
            .get(id=kwargs.get('show_id'))
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
        return kwargs
