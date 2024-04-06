from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Group, Post, User, Comment, Follow
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models.functions import Lower


# @cache_page(20, key_prefix='index_page')
def index(request):
    keyword = request.GET.get('q', None)
    post_list = Post.objects.select_related('author').select_related('group').annotate(text_lower=Lower('text')).filter(text_lower__icontains=keyword).order_by('-pub_date') if keyword else Post.objects.order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, "keyword": keyword,}
    )
        
    
def group_posts(request, slug):
    def get_object_or_404(Group, slug):
        groups = Group.objects.filter(slug=slug)
        return groups.first()
    
    group = get_object_or_404(Group, slug=slug) 
    print(group)
    if not group:
        return HttpResponse(status=404)
    
    posts = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, 
                  'group.html', 
                  {'group': group, 'posts': posts, 'paginator': paginator, 'page': page}
                  )

@login_required
def new_post(request):
    is_edit = False
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {'form': form, 'is_edit': is_edit})


def profile(request, username):
        author = User.objects.get(username=username)
        following = bool(Follow.objects.filter(user=request.user, author=author).count())
        posts = Post.objects.filter(author_id=author.id)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        count = posts.count()
        return render(request, 'profile.html', {'author': author, 'count': count, 'page': page, 'paginator': paginator, 'following': following, 'profile': author})
    
    
def post_view(request, username, post_id):
    form = CommentForm()
    author = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    items = Comment.objects.filter(post_id=post_id).order_by('-created')
    count = Post.objects.filter(author_id=author.id).count()
    return render(request, 'post.html', {'author': author, 'post': post, 'count': count, 
                                         'form': form, 'items': items}
                  )

@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username, post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    print(form.as_p())
    print(10)
    is_edit = True
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            post.text = form.cleaned_data['text']
            post.save()
        return redirect('post', request.user.username, post_id)
    return render(request, 'new_post.html', {'form': form, 'is_edit': is_edit})


@login_required
def post_delete(request, username, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect(request.META['HTTP_REFERER'], username)

@login_required
def add_comment(request, username, post_id):
    form = CommentForm()
    if request.method == 'POST':
        profile = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, pk=post_id, author=profile)
        form = CommentForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
        return redirect('post', username, post_id)
    return render(request, 'comments.html', {'form': form})


@login_required
def follow_index(request):
    keyword = request.GET.get('q', None)
    user = request.user
    authors = Follow.objects.filter(user=user).values('author')
    posts = Post.objects.filter(author__in=authors).order_by('-pub_date')
    posts = Post.objects.select_related('author') \
                        .select_related('group') \
                        .filter(author__in=authors) \
                        .filter(text__icontains=keyword) \
                        .order_by('-pub_date') if keyword else Post.objects \
                                                                    .order_by('-pub_date') \
                                                                    .filter(author__in=authors) \
                                                                    .order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "follow.html", {'page': page, 'paginator': paginator, 'keyword': keyword})

@login_required
def profile_follow(request, username):
    Follow.objects.create(user=request.user, author=User.objects.get(username=username))
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(user=request.user, author=User.objects.get(username=username)).delete()
    return redirect('profile', username)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )
    
    
def server_error(request):
    return render(request, "misc/500.html", status=500)
    
