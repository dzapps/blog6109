"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from accounts.views import (
    login_view,
    register_view,
    logout_view,
)
from posts.views import posts_home

urlpatterns = [
    re_path(r'^$', posts_home),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^comments/', include('comments.urls', namespace='comments')),
    re_path(r'^posts/', include('posts.urls', namespace='posts')),
    re_path(r'^login/', login_view, name='login'),
    re_path(r'^register/', register_view, name='register'),
    re_path(r'^logout/', logout_view, name='logout'),

]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)