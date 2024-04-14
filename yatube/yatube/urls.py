from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls),
    path('practice/', include('practice.urls')),
    path('', include('posts.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
]


urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about-author'),
        path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about-spec'),
        path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT})
]


handler404 = 'posts.views.page_not_found'
handler500 = 'posts.views.server_error'

# при DUBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # при DUBUG = False
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), # штука для статики
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), # штука для медиа
        ]