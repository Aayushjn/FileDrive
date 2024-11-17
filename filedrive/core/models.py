from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_initials(self) -> str:
        return self.first_name[0] + self.last_name[0]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"


class AuditedItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="%(class)s_modified_by", null=True)

    class Meta:
        abstract = True
