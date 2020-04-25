from django.urls import path

from . import views

urlpatterns = [
    path('<int:show_id>/rss/', views.ShowFeed(), name='show_rss'),
]
