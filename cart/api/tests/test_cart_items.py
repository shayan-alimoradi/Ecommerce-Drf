from rest_framework import status
from model_bakery import baker
import pytest

from cart.models import CartItem, Cart
from product.models import Product


@pytest.mark.django_db
def test_create_cart_item_if_valid_data_returns_201(api_client):
    cart = Cart.objects.create()
    product = baker.make(Product)

    response = api_client.post(
        f"/api/v1/cart/{cart.id}/items/",
        data={"cart_id": cart.id, "product_id": product.id, "quantity": 7},
    )

    response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_cart_item_if_invalid_data_returns_400(api_client):
    cart = Cart.objects.create()

    response = api_client.post(f"/api/v1/cart/{cart.id}/items/", data={})

    response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_cart_item_if_cart_item_exists_returns_200(api_client):
    cart = Cart.objects.create()
    product = baker.make(Product)

    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=7)

    response = api_client.get(f"/api/v1/cart/{cart.id}/items/{cart_item.id}/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_cart_item_if_cart_item_not_exists_returns_404(api_client):
    cart = Cart.objects.create()

    response = api_client.get(f"/api/v1/cart/{cart.id}/items/700/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_cart_item_if_data_is_valid_returns_200(api_client):
    cart = Cart.objects.create()
    product = baker.make(Product)

    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=7)

    response = api_client.patch(
        f"/api/v1/cart/{cart.id}/items/{cart_item.id}/", data={"quantity": 9}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["quantity"] == 9


@pytest.mark.django_db
def test_destory_cart_item(api_client):
    cart = Cart.objects.create()
    product = baker.make(Product)

    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=7)

    response = api_client.delete(f"/api/v1/cart/{cart.id}/items/{cart_item.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
