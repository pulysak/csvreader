import csv
import logging
from io import StringIO

import requests
from django.db import DatabaseError
from requests import HTTPError

from .models import Product

logger = logging.getLogger(__name__)


class ProductReader:

    FILE_URL = 'https://drive.google.com/uc?authuser=0&id=1fTb-2kPx3PSvhiGUgKE4fe6VL-cSWQfj&export=download'
    reader_kwargs = {
        'delimiter': ',',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file = None

    def _download_file(self):
        response = requests.get(self.FILE_URL)
        response.raise_for_status()
        self.csv_file = StringIO(response.text)

    def _get_csv(self):
        self._download_file()
        return csv.DictReader(self.csv_file, **self.reader_kwargs)

    def _remove_deleted_products(self, current_skus):
        products_to_delete = Product.objects.exclude(sku__in=current_skus)
        products_to_delete.update(is_deleted=True)
        logger.info(
            'Next products were deleted from the file %s. Mark them as is_deleted',
            products_to_delete.values_list('id', flat=True)
        )

    def update_products(self):
        try:
            csv_file = self._get_csv()
        except HTTPError:
            logger.exception(
                'Http error occurred during getting file. Check that file exists and that file url is correct'
            )
            return

        current_skus = []
        for row in csv_file:
            sku = row.get('sku (unique id)')
            current_skus.append(sku)
            product_kwargs = {
                'name': row.get('product_name'),
                'barcode': row.get('barcode'),
                'photo_url': row.get('photo_url'),
                'price': row.get('price_cents') or None,
                'producer': row.get('producer'),
                'is_deleted': False,
            }

            try:
                product, created = Product.objects.get_or_create(sku=sku, defaults=product_kwargs)
            except DatabaseError:
                logger.exception('DB error occurred trying to write next row - %s', row)
                continue

            if not created:
                product.__dict__.update(product_kwargs)
                product.save()

        self._remove_deleted_products(current_skus)
