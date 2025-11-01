"""
Category domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.permissions import IsAuthenticatedReadOnly
from api.categories.services import category_create, category_update, category_delete
from api.categories.selectors import category_list, category_get_by_id
from api.categories.serializers import (
    CategoryOutputSerializer,
    CategoryCreateInputSerializer,
    CategoryUpdateInputSerializer,
)


class CategoryPagination(PageNumberPagination):
    """Pagination for category list"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListApi(APIView):
    """List and create categories"""
    permission_classes = [IsAuthenticatedReadOnly]
    pagination_class = CategoryPagination
    
    @extend_schema(
        operation_id='categories_list',
        summary='List categories',
        description='List all categories with pagination. Customers have read-only access, staff/admin can create.',
        parameters=[
            OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
            OpenApiParameter('page_size', OpenApiTypes.INT, description='Page size'),
        ],
        responses={
            200: CategoryOutputSerializer(many=True),
        },
        tags=['Categories']
    )
    def get(self, request):
        """Get paginated list of categories"""
        paginator = self.pagination_class()
        
        page_size = paginator.get_page_size(request)
        page = int(request.query_params.get('page', 1))
        
        offset = (page - 1) * page_size
        
        categories, total_count = category_list(
            limit=page_size,
            offset=offset
        )
        
        serializer = CategoryOutputSerializer(categories, many=True)
        
        response_data = {
            'count': total_count,
            'next': None,
            'previous': None,
            'results': serializer.data
        }
        
        if offset + page_size < total_count:
            response_data['next'] = f"{request.path}?page={page + 1}&page_size={page_size}"
        
        if page > 1:
            response_data['previous'] = f"{request.path}?page={page - 1}&page_size={page_size}"
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='categories_create',
        summary='Create a category',
        description='Create a new category. Staff/admin only.',
        request=CategoryCreateInputSerializer,
        responses={
            201: CategoryOutputSerializer,
            400: {'description': 'Validation error'}
        },
        tags=['Categories']
    )
    def post(self, request):
        """Create a new category"""
        serializer = CategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category = category_create(name=serializer.validated_data['name'])
        
        output_serializer = CategoryOutputSerializer(category)
        return Response(
            {
                'message': 'Category created successfully.',
                'category': output_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class CategoryDetailApi(APIView):
    """Get, update, or delete a specific category"""
    permission_classes = [IsAuthenticatedReadOnly]
    
    @extend_schema(
        operation_id='categories_detail',
        summary='Get category details',
        description='Get detailed information about a specific category.',
        responses={
            200: CategoryOutputSerializer,
            404: {'description': 'Category not found'}
        },
        tags=['Categories']
    )
    def get(self, request, category_id):
        """Get category details"""
        category = category_get_by_id(category_id=category_id)
        serializer = CategoryOutputSerializer(category)
        return Response(
            {
                'category': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='categories_update',
        summary='Update a category',
        description='Update an existing category. Staff/admin only.',
        request=CategoryUpdateInputSerializer,
        responses={
            200: CategoryOutputSerializer,
            400: {'description': 'Validation error'},
            404: {'description': 'Category not found'}
        },
        tags=['Categories']
    )
    def put(self, request, category_id):
        """Update a category"""
        serializer = CategoryUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category = category_update(category_id=category_id, name=serializer.validated_data['name'])
        
        output_serializer = CategoryOutputSerializer(category)
        return Response(
            {
                'message': 'Category updated successfully.',
                'category': output_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='categories_delete',
        summary='Delete a category',
        description='Delete a category. Staff/admin only.',
        responses={
            200: {'description': 'Category deleted successfully', 'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}},
            404: {'description': 'Category not found'}
        },
        tags=['Categories']
    )
    def delete(self, request, category_id):
        """Delete a category"""
        category_delete(category_id=category_id)
        return Response(
            {
                'message': 'Category deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

