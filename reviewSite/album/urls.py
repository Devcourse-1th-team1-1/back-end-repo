from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'albums/<int:album_id>/',
        views.AlbumDetailView.as_view(),
        name='album-detail',
    ),
    path('albums/new/', views.AlbumCreateView.as_view(), name='album-create'),
    path(
        'albums/<int:album_id>/edit/',
        views.AlbumUpdateView.as_view(),
        name='album-update',
    ),
    path(
        'albums/<int:album_id>/delete/',
        views.AlbumDeleteView.as_view(),
        name='album-delete',
    ),
    #path(
    #    
    #),
]