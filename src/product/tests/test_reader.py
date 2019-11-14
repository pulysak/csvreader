from io import StringIO
from dataclasses import dataclass

import pytest
from pytest import fixture
from requests.exceptions import HTTPError

from ..reader import ProductReader
from ..models import Product

csv_file_headers = ['sku (unique id)', 'product_name', 'barcode', 'photo_url', 'price_cents', 'producer']


@dataclass
class MockedResponse:

    text: str
    status_code: int

    def raise_for_status(self):
        if self.status_code != 200:
            raise HTTPError()


@fixture
def reader():
    return ProductReader()


@fixture
def csv_text_version1():
    return (
        'product_name,photo_url,barcode,price_cents,sku (unique id),producer\n'
        'Tea - Camomele,http://dummyimage.com/237x192.png/ff4444/ffffff,V8822,71127,0285b967-261a-4a95-a21c-5c797ac7c0a2,McLaughlin-Bosco\n'
        'Eggroll,http://dummyimage.com/103x112.bmp/cc0000/ffffff,99689,94899,0d9803c2-d16d-4f38-826c-f9869f619166,"Weber, Cremin and Hermiston"\n'
        '"Lid - High Heat, Super Clear",http://dummyimage.com/163x140.jpg/dddddd/000000,E8013,89271,049d0c34-238c-47b0-ab49-154a37fbd163,Gislason LLC\n'
    )


@fixture
def csv_file_verison1(csv_text_version1):
    return StringIO(csv_text_version1)

@fixture
def csv_text_version2():
    """
        Added 2new rows
        Deleted one row
        Changed one row
    """

    return (
        'product_name,photo_url,barcode,price_cents,sku (unique id),producer\n'
        'New Name,http://dummyimage.com/237x192.png/ff4444/ffffff,V8822,71127,0285b967-261a-4a95-a21c-5c797ac7c0a2,McLaughlin-Bosco\n'
        '"Lid - High Heat, Super Clear",http://dummyimage.com/163x140.jpg/dddddd/000000,E8013,89271,049d0c34-238c-47b0-ab49-154a37fbd163,Gislason LLC\n'
        'New row1,http://dummyimage.com/103x112.bmp/cc0000/ffffff,7777,8888,9d9803c2-d16d-4f38-826c-f9869f619199,New row producer1\n'
        'New row2,http://dummyimage.com/103x112.bmp/cc0000/ffffff,7777,9999,9d9803c2-d16d-4f38-826c-f9869f619111,New row producer2\n'

    )


@fixture
def csv_file_verison2(csv_text_version2):
    return StringIO(csv_text_version2)


def test_download_file_return_correct_string_io(reader, mocker, csv_text_version1):
    mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    reader._download_file()
    assert type(reader.csv_file) == StringIO
    assert reader.csv_file.read() == csv_text_version1


def test_download_file_raises_http_error(reader, mocker):
    mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=404))
    with pytest.raises(HTTPError):
        reader._download_file()


def test_get_correct_csv_file(reader, mocker, csv_file_verison1, csv_text_version1):
    mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    csv_file = reader._get_csv()

    rows = list(csv_file)
    expected_rows = [
        {
            'product_name': 'Tea - Camomele',
            'photo_url': 'http://dummyimage.com/237x192.png/ff4444/ffffff',
            'barcode': 'V8822',
            'price_cents': '71127',
            'sku (unique id)': '0285b967-261a-4a95-a21c-5c797ac7c0a2',
            'producer': 'McLaughlin-Bosco'
        },
        {
            'product_name': 'Eggroll',
            'photo_url': 'http://dummyimage.com/103x112.bmp/cc0000/ffffff',
            'barcode': '99689',
            'price_cents': '94899',
            'sku (unique id)': '0d9803c2-d16d-4f38-826c-f9869f619166',
            'producer': 'Weber, Cremin and Hermiston'
        },
        {
            'product_name': 'Lid - High Heat, Super Clear',
            'photo_url': 'http://dummyimage.com/163x140.jpg/dddddd/000000',
            'barcode': 'E8013',
            'price_cents': '89271',
            'sku (unique id)': '049d0c34-238c-47b0-ab49-154a37fbd163',
            'producer': 'Gislason LLC'
        },
    ]

    assert len(rows) == 3
    assert rows == expected_rows


@pytest.mark.django_db
def test_update_products_create_products_in_db(reader, csv_text_version1, mocker):
    mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    reader.update_products()

    product1 = Product.objects.get(sku='0285b967-261a-4a95-a21c-5c797ac7c0a2')
    product2 = Product.objects.get(sku='0d9803c2-d16d-4f38-826c-f9869f619166')
    product3 = Product.objects.get(sku='049d0c34-238c-47b0-ab49-154a37fbd163')

    assert Product.objects.active().count() == 3

    assert product1.name == 'Tea - Camomele'
    assert product1.photo_url == 'http://dummyimage.com/237x192.png/ff4444/ffffff'
    assert product1.barcode == 'V8822'
    assert product1.price == 71127
    assert str(product1.sku) == '0285b967-261a-4a95-a21c-5c797ac7c0a2'
    assert product1.producer == 'McLaughlin-Bosco'

    assert product2.name == 'Eggroll'
    assert product2.photo_url == 'http://dummyimage.com/103x112.bmp/cc0000/ffffff'
    assert product2.barcode == '99689'
    assert product2.price == 94899
    assert str(product2.sku) == '0d9803c2-d16d-4f38-826c-f9869f619166'
    assert product2.producer == 'Weber, Cremin and Hermiston'

    assert product3.name == 'Lid - High Heat, Super Clear'
    assert product3.photo_url == 'http://dummyimage.com/163x140.jpg/dddddd/000000'
    assert product3.barcode == 'E8013'
    assert product3.price == 89271
    assert str(product3.sku) == '049d0c34-238c-47b0-ab49-154a37fbd163'
    assert product3.producer == 'Gislason LLC'


@pytest.mark.django_db
def test_update_products_update_products_in_db(reader, csv_text_version1, csv_text_version2, mocker):
    mocked_get = mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    reader.update_products()

    product_to_update = Product.objects.get(sku='0285b967-261a-4a95-a21c-5c797ac7c0a2')
    assert product_to_update.name == 'Tea - Camomele'

    mocked_get.return_value = MockedResponse(text=csv_text_version2, status_code=200)
    reader.update_products()

    updated_product = Product.objects.get(sku='0285b967-261a-4a95-a21c-5c797ac7c0a2')
    assert updated_product.name == 'New Name'


@pytest.mark.django_db
def test_update_products_add_new_products_in_db(reader, csv_text_version1, csv_text_version2, mocker):
    mocked_get = mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    reader.update_products()

    new_sku1 = '9d9803c2-d16d-4f38-826c-f9869f619199'
    new_sku2 = '9d9803c2-d16d-4f38-826c-f9869f619111'
    assert Product.objects.filter(sku=new_sku1).count() == 0
    assert Product.objects.filter(sku=new_sku2).count() == 0

    mocked_get.return_value = MockedResponse(text=csv_text_version2, status_code=200)
    reader.update_products()

    assert Product.objects.filter(sku=new_sku1).count() == 1
    assert Product.objects.filter(sku=new_sku2).count() == 1


@pytest.mark.django_db
def test_update_products_marks_products_as_deleted(reader, csv_text_version1, csv_text_version2, mocker):
    mocked_get = mocker.patch('requests.get', return_value=MockedResponse(text=csv_text_version1, status_code=200))
    reader.update_products()
    assert Product.objects.deleted().count() == 0

    mocked_get.return_value = MockedResponse(text=csv_text_version2, status_code=200)
    reader.update_products()
    assert Product.objects.deleted().count() == 1

    deleted_product = Product.objects.deleted().first()
    assert str(deleted_product.sku) == '0d9803c2-d16d-4f38-826c-f9869f619166'
