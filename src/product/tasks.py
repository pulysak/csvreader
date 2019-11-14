import logging

from .reader import ProductReader

logger = logging.getLogger(__name__)


def update_products():
    reader = ProductReader()
    reader.update_products()
