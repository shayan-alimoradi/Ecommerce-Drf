from rest_framework import status
import pytest

from cart.models import Cart


@pytest.mark.django_db
def test_create_cart(api_client):
    response = api_client.post("/api/cart/")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve_cart(api_client):
    cart = Cart.objects.create()

    response = api_client.get(f"/api/cart/{cart.id}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_destroy_cart(api_client):
    cart = Cart.objects.create()

    response = api_client.delete(f"/api/cart/{cart.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    