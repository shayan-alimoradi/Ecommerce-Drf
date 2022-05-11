# Stdlib imports
import json

# Core django imports
from django.contrib.auth import get_user_model

# 3rd-party imports
from rest_framework import status
from model_bakery import baker
import pytest

# Local imports
from product.models import Category

User = get_user_model()


@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post("/api/v1/category/", category)

    return do_create_category


@pytest.mark.django_db
@pytest.mark.skip
def test_create_category_if_user_is_not_staff_returns_403(api_client):

    response = api_client.post("/api/v1/category/", data={"title": "a"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_category_if_data_is_invalid_returns_400(authenticate, create_category):
    authenticate(is_staff=True)

    response = create_category({})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["title"] is not None
    assert json.loads(response.content) == {"title": ["This field is required."]}


@pytest.mark.django_db
def test_create_category_if_data_is_valid_returns_201(authenticate, create_category):
    authenticate(is_staff=True)

    response = create_category({"title": "a"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] > 0


@pytest.mark.django_db
def test_retrieve_if_category_exists_returns_200(api_client):
    category = baker.make(Category)

    response = api_client.get(f"/api/v1/category/{category.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"id": category.id, "title": category.title}


@pytest.mark.django_db
def test_delete_category_if_user_is_staff_returns_204(authenticate, api_client):
    category = baker.make(Category)
    authenticate(is_staff=True)

    response = api_client.delete(f"/api/v1/category/{category.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_category_if_user_is_not_staff_returns_403(authenticate, api_client):
    category = baker.make(Category)
    authenticate()

    response = api_client.delete(f"/api/v1/category/{category.id}/")

    assert response.status_code == status.HTTP_403_FORBIDDEN
