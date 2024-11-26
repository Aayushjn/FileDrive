import pytest
from core.models import User
from files.models import UploadedItem
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from safedelete import HARD_DELETE_NOCASCADE


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",  # nosec: B106 # pragma: allowlist secret
        first_name="John",
        last_name="Doe",
    )
    assert user.email == "test@example.com"
    assert user.get_initials() == "JD"


@pytest.mark.django_db
def test_uploaded_item_creation():
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",  # nosec: B106 # pragma: allowlist secret
        first_name="John",
        last_name="Doe",
    )
    file = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
    uploaded_item = UploadedItem.objects.create(owner=user, item=file, created_by=user)

    assert Path(uploaded_item.item.name).name.startswith("test")
    assert uploaded_item.size == len(b"Hello, world!")
    assert uploaded_item.file_hash is not None
    assert uploaded_item.owner == user
    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)


@pytest.mark.django_db
def test_uploaded_item_deletion():
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",  # nosec: B106 # pragma: allowlist secret
        first_name="John",
        last_name="Doe",
    )
    file = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
    uploaded_item = UploadedItem.objects.create(owner=user, item=file, created_by=user)

    uploaded_item.delete()
    uploaded_item.refresh_from_db()

    assert uploaded_item.item.name.startswith("trash")
    assert UploadedItem.objects.filter(file_hash=uploaded_item.file_hash).first() is None
    assert UploadedItem.all_objects.filter(file_hash=uploaded_item.file_hash).first() is not None

    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)

    assert UploadedItem.objects.filter(file_hash=uploaded_item.file_hash).first() is None
    assert UploadedItem.all_objects.filter(file_hash=uploaded_item.file_hash).first() is None


@pytest.mark.django_db
def test_deleted_item_restore():
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",  # nosec: B106 # pragma: allowlist secret
        first_name="John",
        last_name="Doe",
    )
    file = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
    uploaded_item = UploadedItem.objects.create(owner=user, item=file, created_by=user)

    uploaded_item.delete()
    uploaded_item.undelete()
    uploaded_item.refresh_from_db()

    assert uploaded_item.item.name.startswith("uploads")
    assert UploadedItem.objects.filter(file_hash=uploaded_item.file_hash).first() is not None

    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)
