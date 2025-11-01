"""
Analytics domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.permissions import IsStaffOrAdmin
from api.common.exceptions import BusinessLogicError
from api.analytics.selectors import (
    analytics_get_most_profitable_categories,
    analytics_get_most_profitable_films
)
from api.analytics.serializers import (
    CategoryProfitOutputSerializer,
    FilmProfitOutputSerializer,
)


class MostProfitableCategoriesApi(APIView):
    """Get most profitable categories by year"""
    permission_classes = [IsStaffOrAdmin]
    
    @extend_schema(
        operation_id='analytics_most_profitable_categories',
        summary='Get most profitable categories',
        description='Returns most profitable movie categories grouped by year. Year parameter is optional - if omitted, returns all years. Staff/admin only.',
        parameters=[
            OpenApiParameter('year', OpenApiTypes.INT, description='Filter by year (optional). If not provided, returns all years grouped by year.', required=False),
        ],
        responses={
            200: CategoryProfitOutputSerializer(many=True),
            400: {'description': 'Validation error'},
        },
        tags=['Analytics']
    )
    def get(self, request):
        """Get most profitable categories"""
        year_param = request.query_params.get('year')
        year = int(year_param) if year_param else None
        
        if year_param and not year_param.isdigit():
            return Response(
                {
                    'error': {
                        'type': 'ValidationError',
                        'message': 'Year must be a valid integer.',
                        'code': 'validation_error',
                        'status_code': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            results = analytics_get_most_profitable_categories(year=year)
        except BusinessLogicError as e:
            return Response(
                {
                    'error': {
                        'type': 'BusinessLogicError',
                        'message': str(e),
                        'code': 'business_logic_error',
                        'status_code': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CategoryProfitOutputSerializer(results, many=True)
        return Response(
            {
                'count': len(results),
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )


class MostProfitableFilmsApi(APIView):
    """Get most profitable films by year"""
    permission_classes = [IsStaffOrAdmin]
    
    @extend_schema(
        operation_id='analytics_most_profitable_films',
        summary='Get most profitable films',
        description='Returns most profitable movies grouped by year. Year parameter is optional - if omitted, returns all years. Staff/admin only.',
        parameters=[
            OpenApiParameter('year', OpenApiTypes.INT, description='Filter by year (optional). If not provided, returns all years grouped by year.', required=False),
            OpenApiParameter('limit', OpenApiTypes.INT, description='Maximum number of results (default 100, max 1000)', required=False),
        ],
        responses={
            200: FilmProfitOutputSerializer(many=True),
            400: {'description': 'Validation error'},
        },
        tags=['Analytics']
    )
    def get(self, request):
        """Get most profitable films"""
        year_param = request.query_params.get('year')
        limit_param = request.query_params.get('limit', '100')
        
        year = int(year_param) if year_param else None
        limit = int(limit_param) if limit_param else 100
        
        if year_param and not year_param.isdigit():
            return Response(
                {
                    'error': {
                        'type': 'ValidationError',
                        'message': 'Year must be a valid integer.',
                        'code': 'validation_error',
                        'status_code': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if limit_param and not limit_param.isdigit():
            return Response(
                {
                    'error': {
                        'type': 'ValidationError',
                        'message': 'Limit must be a valid integer.',
                        'code': 'validation_error',
                        'status_code': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            results = analytics_get_most_profitable_films(year=year, limit=limit)
        except BusinessLogicError as e:
            return Response(
                {
                    'error': {
                        'type': 'BusinessLogicError',
                        'message': str(e),
                        'code': 'business_logic_error',
                        'status_code': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FilmProfitOutputSerializer(results, many=True)
        return Response(
            {
                'count': len(results),
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )

