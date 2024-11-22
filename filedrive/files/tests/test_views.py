from pathlib import Path
import pytest
from django.urls import reverse
from core.models import User
from files.models import UploadedItem
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from safedelete import HARD_DELETE_NOCASCADE

@pytest.mark.django_db
def test_home_view(client):
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",
        first_name="John", 
        last_name="Doe", 
    )
    client.force_login(user)
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "Home" in response.context["crumb_title"]


@pytest.mark.django_db
def test_file_uploaded_fully(client, create_user):
    user = create_user(email="test@example.com", password="password123")
    client.force_login(user)

    file_data = SimpleUploadedFile("test.txt", b"Hello, World!", content_type="text/plain")
    url = reverse("upload")
    response = client.post(url, {"file": file_data})

    assert response.status_code in [200, 302]


    uploaded_item = UploadedItem.objects.first()
    assert uploaded_item is not None
    assert uploaded_item.owner == user
    assert Path(uploaded_item.item.name).name.startswith("test")
    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)

