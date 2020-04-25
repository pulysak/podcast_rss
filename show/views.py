from show.base_view import BaseFeedView
from show.feed import AppleFeed, SpotifyFeed


class ShowAppleFeed(BaseFeedView):
    feed_type = AppleFeed


class ShowSpotifyFeed(ShowAppleFeed):
    feed_type = SpotifyFeed
