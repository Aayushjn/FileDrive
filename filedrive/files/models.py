from hashlib import sha1
from pathlib import Path

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from safedelete.managers import SafeDeleteManager
from safedelete.models import HARD_DELETE_NOCASCADE
from safedelete.models import HARD_DELETE
from safedelete.models import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from core.models import AuditedItem

def _get_upload_path(instance: "UploadedItem", filename: str) -> str:
    return f"uploads/{instance.owner.pk}/{Path(filename).name}"


class UploadedItemManager(SafeDeleteManager):
    def create(self, **kwargs):
        item = super().create(**kwargs)
        item.file_hash = sha1(f"{item.owner.email}---{item.name}".encode()).hexdigest()
        item.save()
        return item


class UploadedItem(SafeDeleteModel, AuditedItem):
    _safedelete_policy = SOFT_DELETE_CASCADE

    owner = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="owner")
    item = models.FileField(upload_to=_get_upload_path)
    file_hash = models.CharField(max_length=20, unique=True)

    @property
    def name(self):
        return Path(self.item.name).name

    @property
    def size(self):
        return self.item.size

    def get_absolute_url(self):
        return reverse_lazy("file", kwargs={"file_hash": self.file_hash})
    
    def delete(self, force_policy: int | None = None, **kwargs):
        if force_policy == HARD_DELETE or force_policy == HARD_DELETE_NOCASCADE:
            self.item.delete()
        else:
            old_name = self.item.name
            actual_name = old_name.split("/", 1)[1]
            self.item.storage.save(f"trash/{actual_name}", self.item.file)
            self.item.name = f"trash/{actual_name}"
            self.save(update_fields=("item",))
        return super().delete(force_policy, **kwargs)

    def __str__(self) -> str:
        return self.name

    objects = UploadedItemManager()

    class Meta:
        verbose_name = _("uploaded item")
        verbose_name_plural = _("uploaded items")
        db_table = "uploaded_items"
