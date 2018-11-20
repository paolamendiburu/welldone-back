from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
# Register your models here.
from articles.models import Article, Category, Favorite, Follow, Comment, User


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Comment)





admin.site.site_header = 'WellDone Admin'
admin.site.site_title = 'WellDone Admin'
admin.site.index_title = 'Dashboard'
