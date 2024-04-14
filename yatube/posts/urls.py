from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import api_views, views

router = SimpleRouter()
router.register('posts', api_views.PostViewSet)

urlpatterns = [
    path('<str:username>/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('new/', views.new_post, name='new_post'),
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path('<str:username>/', views.profile, name='profile'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('', views.index, name='index'),
    
    
    # path('api/v1/posts/<int:pk>/', api_views.APIPostDetail.as_view(), name='get_post'),
    # path('api/v1/posts/', api_views.APIPost.as_view(), name='api_posts'),
    path('api/v1/', include(router.urls)),
    
]

