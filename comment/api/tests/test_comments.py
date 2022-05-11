# Stdlib imports
import json

# Core Django imports
from django.contrib.auth import get_user_model

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from product.models import Product
from comment.models import Comment

User = get_user_model()


@pytest.mark.django_db
def test_get_all_comments_returns_200(api_client):
    product = baker.make(Product)
    response = api_client.get(f"/api/v1/products/{product.id}/comments/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_one_comment_returns_200(api_client):
    product = baker.make(Product)
    comment = baker.make(Comment)
    response = api_client.get(f"/api/v1/products/{product.id}/comments/{comment.id}/")

    response_content = json.loads(response.content)

    assert response.status_code == status.HTTP_200_OK
    assert response_content.get("content") == comment.content
    assert response_content.get("object_id") == comment.object_id


@pytest.mark.django_db
@pytest.mark.skip
def test_create_comment_if_user_is_authenticated(api_client, authenticate):
    authenticate(is_staff=True)
    user = api_client.post(
        "/api/v1/sign-up-test/",
        data={
            "username": "test",
            "email": "test@email.com",
            "password": "1QAZqaz!abc",
        },
    )
    user_content = json.loads(user.content)
    print(user_content)

    jwt_token = api_client.post(
        "/api/token/",
        data={
            "username": user_content["username"],
            "password": "1QAZqaz!abc",
        },
    )
    jwt_content = json.loads(jwt_token.content)
    header = {"Authorization": f"Bearer {jwt_content['access']}"}

    product = api_client.post(
        "/api/v1/products/",
        data={
            "title": "a",
            "unit_price": 700,
            "amount": 70,
        },
    )
    product_content = json.loads(product.content)
    print(product_content)

    response = api_client.post(
        f"/api/v1/products/{product_content['id']}/comments/",
        data={
            "author_id": user_content["id"],
            "content": "hello",
            "content_type": product_content.get_content_type,
            "object_id": product_content['id'],
        },
        **header
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.skip
def test_create_comment_if_user_is_not_authenticated(api_client):
    product = baker.make(Product)
    user = baker.make(User)

    response = api_client.post(
        f"/api/v1/products/{product.id}/comments/",
        data={
            "author_id": user.id,
            "content": "hello",
            "content_type": product.get_content_type,
            "object_id": product.id,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_comment_if_user_is_not_authenticated(api_client):
    product = baker.make(Product)
    user = baker.make(User)
    comment = baker.make(Comment)

    response = api_client.patch(
        f"/api/v1/products/{product.id}/comments/{comment.id}/",
        data={
            "author_id": user.id,
            "content": "hello",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_comment_if_user_is_not_the_author(api_client, authenticate):
    authenticate()
    product = baker.make(Product)
    user = baker.make(User)
    comment = baker.make(Comment)

    response = api_client.patch(
        f"/api/v1/products/{product.id}/comments/{comment.id}/",
        data={
            "author_id": user.id,
            "content": "hello",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_comment_if_user_is_not_authenticated(api_client):
    product = baker.make(Product)
    comment = baker.make(Comment)

    response = api_client.delete(
        f"/api/v1/products/{product.id}/comments/{comment.id}/"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_comment_if_user_is_not_the_author(api_client, authenticate):
    authenticate()
    product = baker.make(Product)
    comment = baker.make(Comment)

    response = api_client.patch(f"/api/v1/products/{product.id}/comments/{comment.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN
