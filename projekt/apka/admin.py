from django.contrib import admin
from .models import Post, Like, Hashtag, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Hashtag)
admin.site.register(Comment)
