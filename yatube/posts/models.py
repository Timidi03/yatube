from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    
    
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


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return self.title
    
    
    
