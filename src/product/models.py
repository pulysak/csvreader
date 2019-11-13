from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):

    sku = models.UUIDField(_('SKU'), unique=True)
    name = models.CharField(_('Name'), max_length=255)
    barcode = models.CharField(_('Barcode'), max_length=10)
    photo_url = models.URLField(_('Photo url'), blank=True)
    price = models.IntegerField(_('Price in cents'))
    producer = models.CharField(_('Producer'), max_length=255, blank=True)

    is_deleted = models.BooleanField(_('Is deleted'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f'{self.sku} - {self.name}'
