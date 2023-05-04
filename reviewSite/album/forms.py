from django import forms
from .models import *



class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'title',
            'image1',
            'image2',
            'image3',
        ]
        exclude = ()
        
