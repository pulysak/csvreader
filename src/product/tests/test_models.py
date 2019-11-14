import pytest
from pytest import fixture
from ..models import Product


@fixture
def deleted_and_active_products():
    return [
        Product.objects.create(is_deleted=True, sku='0285b967-261a-4a95-a21c-5c797ac7c0a1', price=1),
        Product.objects.create(is_deleted=True, sku='0285b967-261a-4a95-a21c-5c797ac7c0a2', price=2),
        Product.objects.create(is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a3', price=3),
        Product.objects.create(is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a4', price=4),
        Product.objects.create(is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a5', price=5),
    ]


@pytest.mark.django_db
def test_product_active(deleted_and_active_products):
    assert Product.objects.active().count() == 3


@pytest.mark.django_db
def test_product_deleted(deleted_and_active_products):
    assert Product.objects.deleted().count() == 2
