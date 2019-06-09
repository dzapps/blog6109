from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from uuslug import slugify

from markdown_deux import markdown

from comments.models import Comment
# Create your models here.

class PostManager(models.Manager):
    def emotion(self, *args, **kwargs):
        if args[0]:
            return super(PostManager, self).filter(
                Q(draft=True) |
                ~Q(slug__icontains='interview')

            )
        else:
            return super(PostManager, self).filter(
                Q(draft=False) &
                Q(publish__lte=timezone.now()) &
                ~Q(slug__icontains='interview')

            )

    def interview(self, *args, **kwargs):
        if args[0]:
            return super(PostManager, self).filter(
                Q(draft=True) |
                Q(slug__icontains='interview')
            )
        else:
            return super(PostManager, self).filter(
                Q(draft=False) &
                Q(publish__lte=timezone.now()) &
                Q(slug__icontains='interview')
            )

def upload_location(instance, filename):
    return '%s/%s'%(instance.user, filename)

    # filebase, extension = filename.split('.')         This may break if there is a period in the image name
    # return '%s/%s.%s' %(instance.id, instance.id, extension)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    # The library Pillow is necessary for ImageField
    image = models.ImageField(
                upload_to=upload_location,
                null=True,
                blank=True,
                height_field='height_field',
                width_field='width_field'
        )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-timestamp', '-update']

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)