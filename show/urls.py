from django.urls import path

from . import views

urlpatterns = [
    path('<int:show_id>/apple_feed/', views.ShowAppleFeed(), name='show_apple_rss'),
    path('<int:show_id>/spotify_feed/', views.ShowSpotifyFeed(), name='show_spotify_rss'),
]
