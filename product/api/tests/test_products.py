# Stdlib imports
import json

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from product.models import Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post("/api/v1/products/", product)

    return do_create_product


@pytest.mark.django_db
def test_create_product_if_user_is_not_staff_returns_403(authenticate, create_product):
    authenticate()

    response = create_product(
        {
            "title": "a",
            "unit_price": 700,
            "amount": 70,
        }
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_product_if_data_is_invalid_returns_400(authenticate, create_product):
    authenticate(is_staff=True)

    response = create_product({})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.skip
def test_create_product_if_data_is_valid_returns_201(authenticate, create_product):
    authenticate(is_staff=True)

    response = create_product(
        {
            "title": "a",
            "unit_price": 700,
            "amount": 70,
        }
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve_if_product_exists_returns_200(api_client):
    product = baker.make(Product)

    response = api_client.get(f"/api/v1/products/{product.id}/")

    response_content = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_content["title"] == product.title
    assert response_content["unitPrice"] == float(product.unit_price)


@pytest.mark.django_db
def test_retrieve_if_product_not_exists_returns_404(api_client):
    response = api_client.get(f"/api/v1/products/700/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_product_if_user_is_staff_returns_204(authenticate, api_client):
    product = baker.make(Product)
    authenticate(is_staff=True)

    response = api_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_product_if_user_is_not_staff_returns_403(authenticate, api_client):
    product = baker.make(Product)
    authenticate()

    response = api_client.delete(f"/api/v1/products/{product.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN
