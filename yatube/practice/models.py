from django.db import models
from django.forms import ModelForm

    
GENRE_CHOICES = (
    ("R", "Рок"),
    ("E", "Электроника"),
    ("P", "Поп"),
    ("C", "Классика"),
    ("O", "Саундтреки"),
)


class CD(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    artist = models.CharField(max_length=40)
    date = models.DateField()
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    
    def __repr__(self):
        return "Вот я такой кросавчик"
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_answered = models.BooleanField(default=False)
    

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'body']
