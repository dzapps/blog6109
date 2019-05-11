from django.contrib import admin

from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'update','timestamp']
    list_display_links = ['title']
    list_filter = ['update', 'timestamp']
    search_fields = ['title', 'content']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
