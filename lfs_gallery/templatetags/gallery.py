# -*- coding: utf-8 -*-
from django.template import Library
from django.template.context import RequestContext
from lfs_gallery.models import Gallery, GalleryItem

register = Library()


@register.inclusion_tag('gallery.html', takes_context=True)
def gallery(context, id=1):

    request = context.get("request")
    try:
        items = Gallery.objects.get(id=id).items()
    except Gallery.DoesNotExist:
        items = GalleryItem.objects.none()
    for item in items:
        if request.path.find(item.link) != -1:
            item.selected = True
            break

    return RequestContext(request, {
        "items" : items,
        "MEDIA_URL" : context.get("MEDIA_URL"),
    })
