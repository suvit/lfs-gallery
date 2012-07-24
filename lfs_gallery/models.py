# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from django.conf import settings

CACHE_PREFIX = settings.CACHE_MIDDLEWARE_KEY_PREFIX


class Gallery(models.Model):

    title = models.CharField(verbose_name=u"Название",
                             max_length=100,
                             blank=True, unique=True)

    class Meta:
        ordering = ("title",)

    def __unicode__(self):
        return self.title

    def items(self):
        return self.all_items().filter(active=True)

    def all_items(self):
        return GalleryItem.objects.filter(gallery=self).order_by('position')


class GalleryItem(models.Model):

    gallery = models.ForeignKey(Gallery, verbose_name=u"Галерея")

    title = models.CharField(verbose_name=u"Название", max_length=100)

    link = models.CharField(verbose_name=u"Ссылка", blank=True, max_length=100)

    active = models.BooleanField(verbose_name=u"Активно", default=False)

    position = models.IntegerField(verbose_name=u"Позиция", default=999)

    image = models.ImageField(verbose_name=u"Картинка",
                              upload_to='gallery')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering=("position", )
