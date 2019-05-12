from django.urls import path, re_path

from .views import (
    posts_home,
    posts_list,
    posts_create,
    posts_detail,
    posts_update,
    posts_delete,
)

app_name = 'posts'
urlpatterns = [
    re_path(r'posts/create/', posts_create),
    re_path(r'posts/(?P<slug>[\w-]+)/edit$', posts_update, name='update'),
    re_path(r'posts/(?P<slug>[\w-]+)$', posts_detail, name='detail'),
    re_path(r'posts/delete/', posts_delete),
    re_path(r'posts/', posts_list, name='list'),
    re_path(r'', posts_home),
]
