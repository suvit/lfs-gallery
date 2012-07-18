from django.conf.urls.defaults import *

urlpatterns = patterns('pwgallery.views',

    url(r'^manage/add_gallery/$', "add_gallery", name="add_gallery"),
    url(r'^manage/del_gallery/(?P<id>\d*)/$', "del_gallery", name="del_gallery"),

    url(r'^manage/add_gallery_item/$', "add_gallery_item", name="add_gallery_item"),
    url(r'^manage/del_gallery_item/(?P<id>\d*)/$', "del_gallery_item", name="del_gallery_item"),

    url(r'^manage/manage_gallery_items/$', "manage_gallery_items", name="manage_gallery_items"),
    url(r'^manage/manage_gallery_item/(?P<id>\d*)/$', "manage_gallery_item", name="manage_gallery_item"),
)