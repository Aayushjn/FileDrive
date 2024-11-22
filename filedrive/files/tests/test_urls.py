from django.urls import reverse, resolve
from files.views import home, upload, login

def test_home_url_resolves():
    url = reverse("home")
    assert resolve(url).func == home

def test_upload_url_resolves():
    url = reverse("upload")
    assert resolve(url).func == upload

def test_login_url_resolves():
    url = reverse("login")
    assert resolve(url).func == login
