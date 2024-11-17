from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from ..forms import AuthForm
from ..forms import SignupForm


@require_http_methods(["GET", "POST"])
@login_not_required
def login(request: HttpRequest) -> HttpResponse:
    form = AuthForm(request, request.POST or None)
    context = {
        "form": form,
        "btn_text": "Log In",
    }

    if request.method == "GET":
        return render(request, "login.html", context)

    if not form.is_valid():
        if "__all__" in form.errors:
            context["all_errors"] = form.errors["__all__"]
        return render(request, "form.html", context)

    user = authenticate(request, email=form.cleaned_data["username"], password=form.cleaned_data["password"])
    if user is None or not user.is_active:
        return HttpResponseClientRedirect(reverse("login"))

    auth_login(request, user)
    return HttpResponseClientRedirect(reverse("home"))


@require_http_methods(["GET", "POST"])
@login_not_required
def signup(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST or None)
    context = {
        "form": form,
        "btn_text": "Sign Up",
    }

    if request.method == "GET":
        return render(request, "signup.html", context)

    if not form.is_valid():
        if "__all__" in form.errors:
            context["all_errors"] = form.errors["__all__"]
        return render(request, "form.html", context)

    form.save()
    return HttpResponseClientRedirect(reverse("login"))


@require_POST
def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return HttpResponseClientRedirect(reverse("login"))
