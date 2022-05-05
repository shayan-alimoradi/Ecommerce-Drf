# Core django imports
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

# 3rd-party imports
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

# Local imports
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer,
)
from product.models import Product, Category
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilter
    search_fields = ("title", "description")
    ordering_fields = ("created",)

    def get_serializer_class(self):
        if self.action in ["list", "destroy"]:
            return ProductListSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Product.objects.select_related("category").filter(available=True)
        category_id = self.request.query_params.get("category_id")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    # @method_decorator(cache_page(60 * 5))
    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         queryset = Product.objects.get(pk=kwargs["pk"])
    #         serializer = ProductDetailSerializer(queryset).data
    #         related_obj = queryset.tags.similar_objects()[:3]
    #         related_obj = ProductListSerializer(instance=related_obj, many=True).data
    #         return Response({"product": serializer, "related_obj": related_obj})
    #     except Product.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]


class LikeProductAPIView(APIView):
    bad_request_message = "An error has occured"
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product = get_object_or_404(Product, slug=request.data.get("slug"))
        if request.user not in product.like.all():
            product.like.add(request.user)
            return Response({"detail": "Add to like"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        product = get_object_or_404(Product, slug=request.data.get("slug"))
        if request.user in product.like.all():
            product.like.remove(request.user)
            return Response({"detail": "Remove from like"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )


class DislikeProductAPIView(APIView):
    bad_request_message = "An error has occured"
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product = get_object_or_404(Product, slug=request.data.get("slug"))
        if request.user not in product.dislike.all():
            product.dislike.add(request.user)
            return Response({"detail": "Add to dislike"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        product = get_object_or_404(Product, slug=request.data.get("slug"))
        if request.user in product.dislike.all():
            product.dislike.remove(request.user)
            return Response(
                {"detail": "Remove from dislike"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST
        )
