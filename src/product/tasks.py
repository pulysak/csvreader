import requests
from io import StringIO
import csv
import logging

from requests import HTTPError

from .models import Product

logger = logging.getLogger(__name__)


class ProductReader:

    FILE_URL = 'https://drive.google.com/uc?authuser=0&id=1fTb-2kPx3PSvhiGUgKE4fe6VL-cSWQfj&export=download'

    def _download_file(self):
        response = requests.get(self.FILE_URL)
        response.raise_for_status()
        return StringIO(response.text)

    def get_csv(self):
        return csv.DictReader(self._download_file())


def update_products():
    try:
        csv_file = ProductReader().get_csv()
    except HTTPError:
        logger.exception('Http error during getting file')
        return

    current_skus = []

    for row in csv_file:
        sku = row.get('sku (unique id)')
        current_skus.append(sku)
        product_kwargs = {
            'name': row.get('product_name'),
            'barcode': row.get('barcode'),
            'photo_url': row.get('photo_url'),
            'price': row.get('price_cents'),
            'producer': row.get('producer'),
        }
        product, created = Product.objects.get_or_create(sku=sku, defaults=product_kwargs)

        if not created:
            product.__dict__.update(product_kwargs)
            product.save()

        Product.objects.exclude(sku__in=current_skus).update(is_deleted=True)
