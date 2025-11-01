"""
Rental domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.permissions import IsStaffOrAdmin
from api.rentals.services import rental_create, rental_update, rental_delete
from api.rentals.selectors import rental_list, rental_get_by_id
from api.rentals.serializers import (
    RentalListOutputSerializer,
    RentalDetailOutputSerializer,
    RentalCreateInputSerializer,
    RentalUpdateInputSerializer,
)


class RentalPagination(PageNumberPagination):
    """Pagination for rental list"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RentalListApi(APIView):
    """List and create rentals"""
    permission_classes = [IsStaffOrAdmin]
    pagination_class = RentalPagination
    
    @extend_schema(
        operation_id='rentals_list',
        summary='List rentals',
        description='List rentals with pagination and optional filtering. Staff/admin only.',
        parameters=[
            OpenApiParameter('customer_id', OpenApiTypes.INT, description='Filter by customer ID'),
            OpenApiParameter('staff_id', OpenApiTypes.INT, description='Filter by staff ID'),
            OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
            OpenApiParameter('page_size', OpenApiTypes.INT, description='Page size'),
        ],
        responses={
            200: RentalListOutputSerializer(many=True),
        },
        tags=['Rentals']
    )
    def get(self, request):
        """Get paginated list of rentals"""
        paginator = self.pagination_class()
        
        customer_id = request.query_params.get('customer_id')
        staff_id = request.query_params.get('staff_id')
        page_size = paginator.get_page_size(request)
        page = int(request.query_params.get('page', 1))
        
        offset = (page - 1) * page_size
        
        rentals, total_count = rental_list(
            customer_id=int(customer_id) if customer_id else None,
            staff_id=int(staff_id) if staff_id else None,
            limit=page_size,
            offset=offset
        )
        
        serializer = RentalListOutputSerializer(rentals, many=True)
        
        response_data = {
            'count': total_count,
            'next': None,
            'previous': None,
            'results': serializer.data
        }
        
        if offset + page_size < total_count:
            query_params = f"page={page + 1}&page_size={page_size}"
            if customer_id:
                query_params += f"&customer_id={customer_id}"
            if staff_id:
                query_params += f"&staff_id={staff_id}"
            response_data['next'] = f"{request.path}?{query_params}"
        
        if page > 1:
            query_params = f"page={page - 1}&page_size={page_size}"
            if customer_id:
                query_params += f"&customer_id={customer_id}"
            if staff_id:
                query_params += f"&staff_id={staff_id}"
            response_data['previous'] = f"{request.path}?{query_params}"
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='rentals_create',
        summary='Create a rental',
        description='Create a new rental. Staff/admin only.',
        request=RentalCreateInputSerializer,
        responses={
            201: RentalDetailOutputSerializer,
            400: {'description': 'Validation error'}
        },
        tags=['Rentals']
    )
    def post(self, request):
        """Create a new rental"""
        serializer = RentalCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rental = rental_create(**serializer.validated_data)
        
        output_serializer = RentalDetailOutputSerializer(rental)
        return Response(
            {
                'message': 'Rental created successfully.',
                'rental': output_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class RentalDetailApi(APIView):
    """Get, update, or delete a specific rental"""
    permission_classes = [IsStaffOrAdmin]
    
    @extend_schema(
        operation_id='rentals_detail',
        summary='Get rental details',
        description='Get detailed information about a specific rental. Staff/admin only.',
        responses={
            200: RentalDetailOutputSerializer,
            404: {'description': 'Rental not found'}
        },
        tags=['Rentals']
    )
    def get(self, request, rental_id):
        """Get rental details"""
        rental = rental_get_by_id(rental_id=rental_id)
        serializer = RentalDetailOutputSerializer(rental)
        return Response(
            {
                'rental': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='rentals_update',
        summary='Update a rental',
        description='Update an existing rental. Staff/admin only.',
        request=RentalUpdateInputSerializer,
        responses={
            200: RentalDetailOutputSerializer,
            400: {'description': 'Validation error'},
            404: {'description': 'Rental not found'}
        },
        tags=['Rentals']
    )
    def put(self, request, rental_id):
        """Update a rental"""
        serializer = RentalUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rental = rental_update(rental_id=rental_id, **serializer.validated_data)
        
        output_serializer = RentalDetailOutputSerializer(rental)
        return Response(
            {
                'message': 'Rental updated successfully.',
                'rental': output_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='rentals_delete',
        summary='Delete a rental',
        description='Delete a rental. Staff/admin only.',
        responses={
            200: {'description': 'Rental deleted successfully', 'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}},
            404: {'description': 'Rental not found'}
        },
        tags=['Rentals']
    )
    def delete(self, request, rental_id):
        """Delete a rental"""
        rental_delete(rental_id=rental_id)
        return Response(
            {
                'message': 'Rental deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

