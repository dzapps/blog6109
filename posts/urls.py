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
    re_path(r'^(?P<category>[\w-]+)/list/$', posts_list, name='list'),
    re_path(r'^create/$', posts_create, name='create'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', posts_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/$', posts_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', posts_delete, name='delete'),

]
