from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from .models import User


admin.site.unregister([Group])


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass
