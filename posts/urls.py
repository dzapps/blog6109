from django.urls import path, re_path

from .views import (
    posts_list,
    posts_create,
    posts_detail,
    posts_update,
    posts_delete,
)

app_name = 'posts'
urlpatterns = [
    re_path(r'create/$', posts_create),
    re_path(r'(?P<slug>[\w-]+)/edit$', posts_update, name='update'),
    re_path(r'(?P<slug>[\w-]+)$', posts_detail, name='detail'),
    re_path(r'delete/', posts_delete),
    re_path(r'', posts_list, name='list'),
]
