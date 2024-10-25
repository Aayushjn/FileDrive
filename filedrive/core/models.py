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
        return self.email

    def __repr__(self) -> str:
        return f"User(email={self.email}, first_name={self.first_name}, last_name={self.last_name}, is_active={self.is_active}, is_staff={self.is_staff}, is_superuser={self.is_superuser})"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"


class AuditedItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="modified_by", null=True)

    class Meta:
        abstract = True
