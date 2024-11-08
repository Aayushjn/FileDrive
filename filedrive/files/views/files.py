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

from ..models import UploadedItem


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    items = UploadedItem.objects.filter(owner=request.user)
    size = 0
    for item in items:
        size += item.item.size

    context = {"uploaded_items": UploadedItem.objects.filter(owner=request.user), "consumed": {"total": size, "percent": size / settings.STORAGE_LIMIT * 100}}
    return render(request, "files/home.html", context)


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    UploadedItem.objects.create(owner=request.user, item=request.FILES["file"], created_by=request.user)
    return HttpResponseClientRefresh()


@require_http_methods(["GET", "DELETE"])
def file(request: HttpRequest, file_hash: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem, file_hash=file_hash)
    if request.method == "GET":
        return FileResponse(item.item.open("rb"), as_attachment=True, filename=item.name)

    item.delete()
    return HttpResponseClientRefresh() # TODO: refresh only if len(files) == 0
