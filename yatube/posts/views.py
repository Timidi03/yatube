from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Group, Post
from .forms import PostForm
import datetime as dt

def index(request):
    # posts = Post.objects \
    #     .filter(text__contains='утро') \
    #     .filter(author__username='leo') \
    #     .filter(pub_date__range=(dt.datetime(1854, 7, 7), dt.datetime(1854, 7, 21)))
    # return render(request, 'index.html', {'posts': posts})

    keyword = request.GET.get('q', None)
    posts = Post.objects.select_related('author').select_related('group').filter(text__contains=keyword) if keyword else None
    return render(request, "index.html", {"posts": posts, "keyword": keyword})
        
    
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


def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        group = Group.objects.filter(slug=form.cleaned_data['group'])
        group = group.first() if group else None
        Post.objects.create(
            text = form.cleaned_data['text'],
            author = request.user,
            group = group
        )
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})
    
