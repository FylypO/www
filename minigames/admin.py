from django.contrib import admin
from .models import Game, Post, Comment, Review, User, Profile

# Register your models here.
admin.site.register(Game)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Profile)
