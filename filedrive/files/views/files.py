from django.conf import settings
from django.http import HttpRequest
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRefresh
from safedelete import HARD_DELETE_NOCASCADE

from ..models import UploadedItem


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    items = UploadedItem.objects.filter(owner=request.user)
    size = 0
    for item in items:
        size += item.item.size

    context = {"crumb_title": "Home", "uploaded_items": items, "consumed": {"total": size, "percent": size / settings.STORAGE_LIMIT * 100}}
    return render(request, "files/drive.html", context)

@require_GET
def shared_with_me(request: HttpRequest) -> HttpResponse:
    items = UploadedItem.objects.filter(owner=request.user)
    size = 0
    for item in items:
        size += item.item.size

    context = {"crumb_title": "Shared With Me", "uploaded_items": items, "consumed": {"total": size, "percent": size / settings.STORAGE_LIMIT * 100}}
    return render(request, "files/drive.html", context)

@require_GET
def trash(request: HttpRequest) -> HttpResponse:
    items = UploadedItem.deleted_objects.filter(owner=request.user)
    size = 0
    for item in items:
        size += item.item.size

    context = {"crumb_title": "Home", "uploaded_items": items, "consumed": {"total": size, "percent": size / settings.STORAGE_LIMIT * 100}}
    return render(request, "files/drive.html", context)


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    item = UploadedItem.objects.create(owner=request.user, item=request.FILES["file"], created_by=request.user)
    return render(request, "files/table_item.html", {"item": item})


@require_http_methods(["GET", "DELETE"])
def file(request: HttpRequest, file_hash: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem.all_objects, file_hash=file_hash)
    if request.method == "GET":
        return FileResponse(item.item.open("rb"), as_attachment=True, filename=item.name)

    force_policy = None
    manager = UploadedItem.objects
    if item.deleted is not None:
        force_policy = HARD_DELETE_NOCASCADE
        manager = UploadedItem.deleted_objects
    
    item.delete(force_policy=force_policy)
    if manager.filter(owner=request.user).count() == 0:
        return HttpResponseClientRefresh()
    return HttpResponse()
