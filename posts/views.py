from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .form import PostForm
from .models import Post
# Create your views here.

def posts_home(request):
    intro = get_object_or_404(Post, title='設站緣由')
    content = {
        'intro': intro,
    }
    return render(request, 'index.html', content)

def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, '成功建立！')
        return HttpResponseRedirect(instance.get_absolute_url())

    content = {
        'form': form,
        'title': '建立貼文',
    }
    return render(request, 'post_form.html', content)

def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    previous_page = request.META.get('HTTP_REFERER', '/')

    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id,

    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid()and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj=None

        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                                user=request.user,
                                content_type=content_type,
                                object_id=obj_id,
                                content=content_data,
                                parent=parent_obj,
                            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments

    content = {
        'instance': instance,
        'comments': comments,
        'comment_form': form,
        'previous': previous_page,

    }

    return render(request, 'post_detail.html', content)

def posts_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, '已儲存！')
        return HttpResponseRedirect(instance.get_absolute_url())

    content = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }

    return render(request, 'post_form.html', content)

def posts_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, '成功刪除！')
    return redirect('posts:list')

def posts_list(request, category=None):
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.query(True, category)
    else:
        queryset_list = Post.objects.query(False, category)

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    content = {
        'object_list': queryset,
        'title': '心情點滴',
        'page_request_var': page_request_var,
        'today': timezone.now().date(),

    }

    return render(request, 'post_list.html', content)

# def posts_tech_list(request):
#     if request.user.is_staff or request.user.is_superuser:
#         queryset_list = Post.objects.query(True, 'tech')
#     else:
#         queryset_list = Post.objects.query(False, 'tech')
#
#     query = request.GET.get('q')
#     if query:
#         queryset_list = queryset_list.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(user__first_name__icontains=query) |
#             Q(user__last_name__icontains=query)
#         ).distinct()
#
#     paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
#
#     page_request_var = 'page'
#     page = request.GET.get(page_request_var)
#     queryset = paginator.get_page(page)
#
#     content = {
#         'object_list': queryset,
#         'title': '心情點滴',
#         'page_request_var': page_request_var,
#         'today': timezone.now().date(),
#
#     }
#
#     return render(request, 'post_list.html', content)
#
# def posts_interview_list(request):
#     if request.user.is_staff or request.user.is_superuser:
#         queryset_list = Post.objects.query(True, 'interview')
#     else:
#         queryset_list = Post.objects.query(False, 'interview')
#
#     query = request.GET.get('q')
#     if query:
#         queryset_list = queryset_list.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(user__first_name__icontains=query) |
#             Q(user__last_name__icontains=query)
#         ).distinct()
#
#     paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
#
#     page_request_var = 'page'
#     page = request.GET.get(page_request_var)
#     queryset = paginator.get_page(page)
#
#     content = {
#         'object_list': queryset,
#         'title': '面試心得',
#         'page_request_var': page_request_var,
#         'today': timezone.now().date(),
#
#     }
#
#     return render(request, 'post_list.html', content)
#
# def posts_intern_list(request):
#     if request.user.is_staff or request.user.is_superuser:
#         queryset_list = Post.objects.query(True, 'intern')
#     else:
#         queryset_list = Post.objects.query(False, 'intern')
#
#     query = request.GET.get('q')
#     if query:
#         queryset_list = queryset_list.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(user__first_name__icontains=query) |
#             Q(user__last_name__icontains=query)
#         ).distinct()
#
#     paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
#
#     page_request_var = 'page'
#     page = request.GET.get(page_request_var)
#     queryset = paginator.get_page(page)
#
#     content = {
#         'object_list': queryset,
#         'title': '暑期實習',
#         'page_request_var': page_request_var,
#         'today': timezone.now().date(),
#
#     }
#
#     return render(request, 'post_list.html', content)