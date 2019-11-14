import pytest
from django.urls import reverse
from ..models import Product


@pytest.fixture
def products():
    return [
        Product.objects.create(is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a1', producer='One_producer'),
        Product.objects.create(is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a2', producer='One_producer'),
        Product.objects.create(is_deleted=True, sku='0285b967-261a-4a95-a21c-5c797ac7c0a3', producer='One_producer'),
        Product.objects.create(
            is_deleted=False, sku='0285b967-261a-4a95-a21c-5c797ac7c0a4', producer='Another producer',
        ),
    ]


@pytest.mark.django_db
def test_product_list_view_get_200(client):
    response = client.get(reverse('product:list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_list_view_filter_by_producer_and_is_deleted(client, products):
    response = client.get(reverse('product:list'))
    assert len(response.json().get('results')) == 3

    response = client.get(f'{reverse("product:list")}?producer=One_producer')
    assert len(response.json().get('results')) == 2
