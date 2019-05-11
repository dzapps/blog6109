from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from uuslug import slugify

# Create your models here.

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    return '%s/%s'%(instance.id, filename)

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