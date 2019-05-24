from django.urls import path, re_path

from .views import (
    comment_thread,

)

app_name = 'comments'
urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    # re_path(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),

]
