from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Post

def index(request):
    latest = Post.objects.order_by('-pub_date')[:10]
    return render(request, 'index.html', {'posts': latest})
        
    
def group_posts(request, slug):
    def get_object_or_404(Group, slug):
        groups = Group.objects.filter(slug=slug)
        return groups.first()
    
    group = get_object_or_404(Group, slug=slug) 
    print(group)
    if not group:
        return HttpResponse(status=404)
    
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})