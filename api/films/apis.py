"""
Film domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.permissions import IsAuthenticatedReadOnly
from api.films.services import film_create, film_update, film_delete
from api.films.selectors import film_list, film_get_by_id
from api.films.serializers import (
    FilmListOutputSerializer,
    FilmDetailOutputSerializer,
    FilmCreateInputSerializer,
    FilmUpdateInputSerializer,
)


class FilmPagination(PageNumberPagination):
    """Pagination for film list"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class FilmListApi(APIView):
    """List and create films"""
    permission_classes = [IsAuthenticatedReadOnly]
    pagination_class = FilmPagination
    
    @extend_schema(
        operation_id='films_list',
        summary='List films',
        description='List films with pagination and optional search. Customers have read-only access, staff/admin can create.',
        parameters=[
            OpenApiParameter('search', OpenApiTypes.STR, description='Search term for title or description'),
            OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
            OpenApiParameter('page_size', OpenApiTypes.INT, description='Page size'),
        ],
        responses={
            200: FilmListOutputSerializer(many=True),
        },
        tags=['Films']
    )
    def get(self, request):
        """Get paginated list of films"""
        paginator = self.pagination_class()
        
        search = request.query_params.get('search', None)
        page_size = paginator.get_page_size(request)
        page = int(request.query_params.get('page', 1))
        
        offset = (page - 1) * page_size
        
        films, total_count = film_list(
            search=search,
            limit=page_size,
            offset=offset
        )
        
        # Serialize response
        serializer = FilmListOutputSerializer(films, many=True)
        
        # Build paginated response
        response_data = {
            'count': total_count,
            'next': None,
            'previous': None,
            'results': serializer.data
        }
        
        if offset + page_size < total_count:
            response_data['next'] = f"{request.path}?page={page + 1}&page_size={page_size}"
            if search:
                response_data['next'] += f"&search={search}"
        
        if page > 1:
            response_data['previous'] = f"{request.path}?page={page - 1}&page_size={page_size}"
            if search:
                response_data['previous'] += f"&search={search}"
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='films_create',
        summary='Create a film',
        description='Create a new film. Staff/admin only.',
        request=FilmCreateInputSerializer,
        responses={
            201: FilmDetailOutputSerializer,
            400: {'description': 'Validation error'}
        },
        tags=['Films']
    )
    def post(self, request):
        """Create a new film"""
        serializer = FilmCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        film = film_create(**serializer.validated_data)
        
        output_serializer = FilmDetailOutputSerializer(film)
        return Response(
            {
                'message': 'Film created successfully.',
                'film': output_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class FilmDetailApi(APIView):
    """Get, update, or delete a specific film"""
    permission_classes = [IsAuthenticatedReadOnly]
    
    @extend_schema(
        operation_id='films_detail',
        summary='Get film details',
        description='Get detailed information about a specific film.',
        responses={
            200: FilmDetailOutputSerializer,
            404: {'description': 'Film not found'}
        },
        tags=['Films']
    )
    def get(self, request, film_id):
        """Get film details"""
        film = film_get_by_id(film_id=film_id)
        serializer = FilmDetailOutputSerializer(film)
        return Response(
            {
                'film': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='films_update',
        summary='Update a film',
        description='Update an existing film. Staff/admin only.',
        request=FilmUpdateInputSerializer,
        responses={
            200: FilmDetailOutputSerializer,
            400: {'description': 'Validation error'},
            404: {'description': 'Film not found'}
        },
        tags=['Films']
    )
    def put(self, request, film_id):
        """Update a film"""
        serializer = FilmUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        film = film_update(film_id=film_id, **serializer.validated_data)
        
        output_serializer = FilmDetailOutputSerializer(film)
        return Response(
            {
                'message': 'Film updated successfully.',
                'film': output_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='films_delete',
        summary='Delete a film',
        description='Delete a film. Staff/admin only.',
        responses={
            200: {'description': 'Film deleted successfully', 'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}},
            404: {'description': 'Film not found'}
        },
        tags=['Films']
    )
    def delete(self, request, film_id):
        """Delete a film"""
        film_delete(film_id=film_id)
        return Response(
            {
                'message': 'Film deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

