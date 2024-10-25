from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("upload", views.upload, name="upload"),
    path("file/<str:file_hash>", views.file, name="file"),
    path("", views.home, name="home"),
]
