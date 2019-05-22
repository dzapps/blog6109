from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from comments.models import Comment
from .form import PostForm
from .models import Post
# Create your views here.

def posts_home(request):
    intro = get_object_or_404(Post, title='設站原由')
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
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    content = {
        'form': form,
    }
    return render(request, 'post_form.html', content)

def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    content_type = ContentType.objects.get_for_model(Post)
    obj_id = instance.id
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)

    content = {
        'instance': instance,
        'comments': comments,
    }

    return render(request, 'post_detail.html', content)

def posts_list(request):
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    else:
        queryset_list = Post.objects.active()

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
        'title': 'List',
        'page_request_var': page_request_var,
        'today': timezone.now().date(),

    }

    return render(request, 'post_list.html', content)

def posts_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, 'Item saved')
        return HttpResponseRedirect(instance.get_absolute_url())

    content = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }

    return render(request, 'post_form.html', content)

def posts_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    messages.success(request, 'Successfully deleted')
    return redirect('post:list')