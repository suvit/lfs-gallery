# -*- coding: utf-8 -*-
# django imports
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

# lfs imports
from lfs.core.utils import set_message_cookie
from lfs.core.widgets.image import LFSImageInput
from lfs_gallery.models import Gallery, GalleryItem


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery


class GalleryItemForm(ModelForm):
    class Meta:
        model = GalleryItem
        widgets = {'image': LFSImageInput,
                  }


@permission_required("core.manage_shop")
def manage_galleries(request):

    try:
        item = GalleryItem.objects.all()[0]
        url = reverse("manage_gallery_item", kwargs={"id": item.id})
    except IndexError:
        url = reverse("add_gallery")

    return HttpResponseRedirect(url)

@permission_required("core.manage_shop")
def manage_gallery_items(request):

    try:
        item = GalleryItem.objects.all()[0]
        url = reverse("manage_gallery_item", kwargs={"id": item.id})
    except IndexError:
        url = reverse("add_gallery_item")

    return HttpResponseRedirect(url)


@permission_required("core.manage_shop")
def manage_gallery_item(request, id, template_name="manage/gallery_item.html"):

    item = get_object_or_404(GalleryItem, pk=id)
    if request.method == "POST":
        form = GalleryItemForm(instance=item,
                               data=request.POST,
                               files=request.FILES)
        if form.is_valid():
            new_action = form.save()
            _update_positions()

            return set_message_cookie(
                url = reverse("manage_gallery_item",
                              kwargs={"id" : item.id}),
                msg = u"Пункт галереи сохранен",
            )
    else:
        form = GalleryItemForm(instance=item)

    return render_to_response(template_name, RequestContext(request, {
        "item" : item,
        "galleries" : Gallery.objects.all(),
        "form" : form,
        "current_id" : int(id),
    }))


@permission_required("core.manage_shop")
def add_gallery_item(request, template_name="manage/add_gallery_item.html"):

    if request.method == "POST":
        form = GalleryItemForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            item = form.save()
            _update_positions()

            return set_message_cookie(
                url = reverse("manage_gallery_item", kwargs={"id" : item.id}),
                msg = u"Пункт галереи добавлен",
            )
    else:
        form = GalleryItemForm()

    return render_to_response(template_name, RequestContext(request, {
        "form" : form,
        "galleries" : Gallery.objects.all(),
    }))


@permission_required("core.manage_shop")
def del_gallery_item(request, id):

    item = get_object_or_404(GalleryItem, pk=id)
    item.delete()

    return set_message_cookie(
        url = reverse("manage_gallery_items"),
        msg = u"Пункт галереи удален",
    )


@permission_required("core.manage_shop")
def add_gallery(request, template_name="manage/add_gallery.html"):

    if request.method == "POST":
        form = GalleryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return set_message_cookie(
                url = reverse("manage_gallery_items"),
                msg = u"Галерея добавлена",
            )
    else:
        form = GalleryForm()

    return render_to_response(template_name, RequestContext(request, {
        "form" : form,
        "galleries" : Gallery.objects.all(),
    }))


@permission_required("core.manage_shop")
def manage_gallery(request, id, template_name="manage/add_gallery.html"):

    gallery = get_object_or_404(Gallery, pk=id)
    form = GalleryForm(instance=gallery,
                       data=request.POST or None,
                       files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            return set_message_cookie(
                url = reverse("manage_gallery", args=[gallery.id]),
                msg = u"Галерея изменена",
            )

    return render_to_response(template_name, RequestContext(request, {
        "form": form,
        'gallery': gallery,
        "galleries" : Gallery.objects.all(),
    }))



@permission_required("core.manage_shop")
def del_gallery(request, id):

    gallery = get_object_or_404(Gallery, pk=id)
    gallery.delete()

    return set_message_cookie(
        url = reverse("manage_gallery_items"),
        msg = u"Галерея удалена",
    )


def _update_positions():

    for gallery in Gallery.objects.all():
        for i, item in enumerate(gallery.items()):
            item.position = (i + 1) * 10
            item.save()
