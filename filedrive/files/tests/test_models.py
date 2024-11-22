import pytest
from core.models import User
from files.models import UploadedItem, SharedItem
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from safedelete import HARD_DELETE, HARD_DELETE_NOCASCADE

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email="test@example.com", password="password123", first_name="John", last_name="Doe")
    assert user.email == "test@example.com"
    assert user.get_initials() == "JD"

@pytest.mark.django_db
def test_uploaded_item_creation():
    user = User.objects.create_user(email="test@example.com", password="password123", first_name="John", last_name="Doe")
    file = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
    uploaded_item = UploadedItem.objects.create(owner=user, item=file, created_by=user)

    assert Path(uploaded_item.item.name).name.startswith("test")
    assert uploaded_item.size == len(b"Hello, world!")
    assert uploaded_item.file_hash is not None
    assert uploaded_item.owner == user
    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)
