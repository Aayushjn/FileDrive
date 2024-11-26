from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http import FileResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRefresh
from safedelete import HARD_DELETE_NOCASCADE

from ..forms import RenameForm
from ..forms import ShareForm
from ..models import SharedItem
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
        # "rename_form": RenameForm(),
        "share_form": ShareForm(user_id=request.user.id),
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
        items=UploadedItem.objects.prefetch_related("shareditem_set").filter(
            shareditem__shared_with=request.user, shareditem__deleted__isnull=True
        ),
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


@require_GET
def modal_form(request: HttpRequest, file_hash: str, action: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem.objects, file_hash=file_hash)
    if item.owner != request.user:
        return HttpResponseClientRefresh(status=403)

    if action == "rename":
        form = RenameForm(item_name=item.name)
        btn_text = "Save Changes"
    elif action == "share":
        form = ShareForm(user_id=request.user.id)
        btn_text = "Share"
    else:
        return HttpResponseBadRequest()
    context = {"url": item.get_absolute_url(), "action": action, "form": form, "btn_text": btn_text}
    return render(request, "files/modal_form.html", context)


@require_http_methods(["GET", "POST", "DELETE"])
def file(request: HttpRequest, file_hash: str) -> HttpResponse:
    item = get_object_or_404(UploadedItem.all_objects, file_hash=file_hash)
    if request.method == "GET":
        return FileResponse(item.item.open("rb"), as_attachment=True, filename=item.name)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "rename":
            form = RenameForm(request.POST, item_name=item.name)
            if form.is_valid():
                item.rename(form.cleaned_data["name"])
                return HttpResponseClientRefresh()
        elif action == "share":
            form = ShareForm(request.POST, user_id=request.user.id)
            if form.is_valid():
                SharedItem.objects.bulk_create(
                    (
                        SharedItem(item=item, shared_with=user, created_by=request.user)
                        for user in form.cleaned_data["share_with"]
                    )
                )
                return HttpResponseClientRefresh()
        elif action == "restore":
            item.undelete()
            return HttpResponse()
        return HttpResponseBadRequest()

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
