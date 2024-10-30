from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST

from .forms import FileUploadForm
from .models import UploadedItem


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    context = {"uploaded_items": UploadedItem.objects.all(), "file_upload_form": FileUploadForm()}
    return render(request, "files/home.html", context)


@require_http_methods(["GET", "POST"])
@login_not_required
def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "files/login.html")

    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)
    if user is None:
        messages.add_message(request, messages.ERROR, "Provided credentials are invalid")
        return redirect(reverse("login"))
    elif not user.is_active:
        messages.add_message(
            request, messages.ERROR, "User is disabled. Contact an administrator for further assistance."
        )
        return redirect(reverse("login"))
    else:
        auth_login(request, user)
        return redirect(reverse("home"))
    
@require_http_methods(["GET", "POST"])
@login_not_required
def signup(request: HttpRequest) -> HttpResponse: # TODO: Replace with signup logic
    if request.method == "GET":
        return render(request, "files/signup.html")

    first_name = request.POST["fname"]
    last_name = request.POST["lname"]
    display_name = request.POST["dname"]
    email = request.POST["email"]
    password = request.POST["password"]
    return redirect(reverse("login"))
    # user = authenticate(request, email=email, password=password)
    # if user is None:
    #     messages.add_message(request, messages.ERROR, "Provided credentials are invalid")
    #     return redirect(reverse("login"))
    # elif not user.is_active:
    #     messages.add_message(
    #         request, messages.ERROR, "User is disabled. Contact an administrator for further assistance."
    #     )
    #     return redirect(reverse("login"))
    # else:
    #     auth_login(request, user)
    #     return redirect(reverse("home"))


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    form = FileUploadForm(request.POST or None, request.FILES or None)
    if not form.is_valid():
        return redirect(reverse("home"))
    UploadedItem.objects.create(owner=request.user, item=form.cleaned_data["file"], created_by=request.user)
    return redirect(reverse("home"))


@require_http_methods(["GET", "DELETE"])
def file(request: HttpRequest, file_hash: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem, file_hash=file_hash)
    if request.method == "GET":
        return FileResponse(item.item.open("rb"), as_attachment=True, filename=item.name)

    item.delete() # maybe actually delete the file from the directory?
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response # TODO: refresh only if len(files) == 0
