from constance.admin import Config
from constance.admin import ConstanceAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from .models import User


admin.site.unregister([Config, Group])


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Config)
class CustomConstanceAdmin(ConstanceAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass
