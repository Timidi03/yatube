from typing import Any
from django import forms
from .models import CD

GENRE_CHOICES = (
    ("R", "Рок"),
    ("E", "Электроника"),
    ("P", "Поп"),
    ("C", "Классика"),
    ("O", "Саундтреки"),
)


class EnhanceFrom(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    title = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=40)
    genre = forms.ChoiceField(choices=GENRE_CHOICES)
    price = forms.DecimalField()
    comment = forms.CharField(widget=forms.Textarea)
    
    def clean_artist(self):
        data = self.cleaned_data['artist']
        if not CD.objects.filter(artist=data):
            raise forms.ValidationError('No artist')
        return data
    