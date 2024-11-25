from django.conf import settings
from django.db.models import QuerySet
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

from ..forms import ShareForm
from ..models import UploadedItem


def drive_view(
    request: HttpRequest, crumb_title: str, show_upload: bool, items: QuerySet[UploadedItem], use_qs_for_size: bool
) -> HttpResponse:
    size = 0
    size_qs = items if use_qs_for_size else UploadedItem.objects.filter(owner=request.user)
    for item in size_qs:
        size += item.item.size

    context = {
        "crumb_title": crumb_title,
        "items": items,
        "consumed": {"total": size, "percent": size / settings.STORAGE_LIMIT * 100},
        "show_upload": show_upload,
        "share_form": ShareForm(request.POST or None, user_id=request.user.id),
    }
    return render(request, "files/drive.html", context)


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return drive_view(
        request,
        crumb_title="Home",
        show_upload=True,
        items=UploadedItem.objects.prefetch_related("owner").filter(owner=request.user),
        use_qs_for_size=True,
    )


@require_GET
def shared_with_me(request: HttpRequest) -> HttpResponse:
    return drive_view(
        request,
        crumb_title="Shared With Me",
        show_upload=False,
        items=UploadedItem.objects.prefetch_related("shareditem_set").filter(shareditem__shared_with=request.user),
        use_qs_for_size=False,
    )


@require_GET
def trash(request: HttpRequest) -> HttpResponse:
    return drive_view(
        request,
        crumb_title="Trash",
        show_upload=False,
        items=UploadedItem.deleted_objects.prefetch_related("owner").filter(owner=request.user),
        use_qs_for_size=False,
    )


@require_POST
def upload(request: HttpRequest) -> HttpResponse:
    item = UploadedItem.objects.create(owner=request.user, item=request.FILES["file"], created_by=request.user)
    return render(request, "files/table_item.html", {"item": item})


@require_http_methods(["GET", "POST", "DELETE"])
def file(request: HttpRequest, file_hash: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem.all_objects, file_hash=file_hash)
    if request.method == "GET":
        return FileResponse(item.item.open("rb"), as_attachment=True, filename=item.name)

    if request.method == "POST":
        print(request.POST)
        print(request.headers)
        return HttpResponse()

    if item.owner != request.user:
        return HttpResponseClientRefresh(status=403)
    force_policy = None
    manager = UploadedItem.objects
    if item.deleted is not None:
        force_policy = HARD_DELETE_NOCASCADE
        manager = UploadedItem.deleted_objects

    item.delete(force_policy=force_policy)
    if manager.filter(owner=request.user).count() == 0:
        return HttpResponseClientRefresh()
    return HttpResponse()
