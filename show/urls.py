from django.urls import path

from . import views

urlpatterns = [
    path('<slug:show_slug>/apple_feed/', views.ShowAppleFeed(), name='show_apple_rss'),
    path('<slug:show_slug>/spotify_feed/', views.ShowSpotifyFeed(), name='show_spotify_rss'),
]
