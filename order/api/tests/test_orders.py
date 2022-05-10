import json

from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
import pytest

from order.models import Order, OrderItem
from cart.models import Cart

User = get_user_model()


@pytest.mark.skip
def test_create_order_if_valid_data_returns_201(api_client):
    # user = baker.make(User)
    user = api_client.post(
        "/api/v1/sign-up/",
        data={
            "username": "test",
            "email": "test@email.com",
            "password": "1QAZqaz!abc",
        },
    )
    user_content = json.loads(user.content)

    jwt_token = api_client.post(
        "/api/token/",
        data={
            "username": user_content["username"],
            "password": user_content["password"],
        },
    )
    jwt_content = json.loads(jwt_token.content)
    header = {"Authorization": f"Bearer {jwt_content['access']}"}

    response = api_client.post(
        "/api/v1/order/",
        data={
            "user_id": user.id,
        },
        **header,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
