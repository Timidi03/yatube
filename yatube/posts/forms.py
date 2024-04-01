from django import forms
from .models import Group

choices = {i.slug:i.title for i in Group.objects.all()}
choices[None] = ''
class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    group = forms.ChoiceField(choices=choices, required=False)
    
