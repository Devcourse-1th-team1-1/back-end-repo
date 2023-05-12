from django.urls import path
from . import views

# app_name = 'album'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        'albums/<int:album_id>/',
        views.AlbumDetailView.as_view(),
        name='album-detail',
    ),
    path(
        'albums/<int:album_id>/comment/',# post 메소드만 받도록 해야함
        views.comment_create,
        name='comment-create',
    )
]