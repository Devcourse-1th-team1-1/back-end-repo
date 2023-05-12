from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'title',
            'poster_src',
            'good_cloud_img',
            'bad_cloud_img',
        ]
        exclude = ()
