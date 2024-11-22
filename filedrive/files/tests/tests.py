import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from safedelete import HARD_DELETE_NOCASCADE

from ..models import UploadedItem


@pytest.mark.django_db
def test_file_uploaded_fully(client, create_user):
    # Create a new user
    user = create_user(email="test@example.com", password="password123")  # nosec

    # Authenticate the user
    client.force_login(user=user)

    # Create a test file
    file_data = SimpleUploadedFile("test.txt", b"Hello, World!", content_type="text/plain")

    # Invoke the '/upload' endpoint
    url = reverse("upload")
    response = client.post(url, {"file": file_data}, format="multipart")

    # Check if the file was uploaded successfully
    assert response.status_code == 200  # Redirect to home page after upload

    # Check if the file is in the database
    uploaded_item = UploadedItem.objects.get(owner=user)
    # assert uploaded_item.name == "test.txt"
    assert uploaded_item.name.startswith("test.txt")
    assert uploaded_item.size == 13  # Size of the file in bytes
    uploaded_item.delete(force_policy=HARD_DELETE_NOCASCADE)
