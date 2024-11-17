from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("upload", views.upload, name="upload"),
    path("file/<str:file_hash>", views.file, name="file"),
    path("trash", views.trash, name="trash"),
    path("shared-with-me", views.shared_with_me, name="shared_with_me"),
    path("", views.home, name="home"),
]
