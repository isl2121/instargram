from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import App, Comment, Tag


admin.site.register(App)
admin.site.register(Comment)
admin.site.register(Tag)