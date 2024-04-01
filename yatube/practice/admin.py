from django.contrib import admin

from .models import CD

class CDAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre']
    
    
    
admin.site.register(CD, CDAdmin)
