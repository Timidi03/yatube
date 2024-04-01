from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('practice/', include('practice.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
