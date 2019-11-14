from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'sku',
        'name',
        'barcode',
        'photo_url',
        'price',
        'producer',
        'created_at',
        'updated_at',
        'is_deleted',
    )
    search_fields = ('producer',)
