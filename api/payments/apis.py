"""
Payment domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.permissions import IsStaffOrAdmin
from api.payments.services import payment_create, payment_update, payment_delete
from api.payments.selectors import payment_list, payment_get_by_id
from api.payments.serializers import (
    PaymentListOutputSerializer,
    PaymentDetailOutputSerializer,
    PaymentCreateInputSerializer,
    PaymentUpdateInputSerializer,
)


class PaymentPagination(PageNumberPagination):
    """Pagination for payment list"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentListApi(APIView):
    """List and create payments"""
    permission_classes = [IsStaffOrAdmin]
    pagination_class = PaymentPagination
    
    @extend_schema(
        operation_id='payments_list',
        summary='List payments',
        description='List payments with pagination and optional filtering. Staff/admin only.',
        parameters=[
            OpenApiParameter('customer_id', OpenApiTypes.INT, description='Filter by customer ID'),
            OpenApiParameter('staff_id', OpenApiTypes.INT, description='Filter by staff ID'),
            OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
            OpenApiParameter('page_size', OpenApiTypes.INT, description='Page size'),
        ],
        responses={
            200: PaymentListOutputSerializer(many=True),
        },
        tags=['Payments']
    )
    def get(self, request):
        """Get paginated list of payments"""
        paginator = self.pagination_class()
        
        customer_id = request.query_params.get('customer_id')
        staff_id = request.query_params.get('staff_id')
        page_size = paginator.get_page_size(request)
        page = int(request.query_params.get('page', 1))
        
        offset = (page - 1) * page_size
        
        payments, total_count = payment_list(
            customer_id=int(customer_id) if customer_id else None,
            staff_id=int(staff_id) if staff_id else None,
            limit=page_size,
            offset=offset
        )
        
        serializer = PaymentListOutputSerializer(payments, many=True)
        
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
        operation_id='payments_create',
        summary='Create a payment',
        description='Create a new payment. Staff/admin only.',
        request=PaymentCreateInputSerializer,
        responses={
            201: PaymentDetailOutputSerializer,
            400: {'description': 'Validation error'}
        },
        tags=['Payments']
    )
    def post(self, request):
        """Create a new payment"""
        serializer = PaymentCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = payment_create(**serializer.validated_data)
        
        output_serializer = PaymentDetailOutputSerializer(payment)
        return Response(
            {
                'message': 'Payment created successfully.',
                'payment': output_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class PaymentDetailApi(APIView):
    """Get, update, or delete a specific payment"""
    permission_classes = [IsStaffOrAdmin]
    
    @extend_schema(
        operation_id='payments_detail',
        summary='Get payment details',
        description='Get detailed information about a specific payment. Staff/admin only.',
        responses={
            200: PaymentDetailOutputSerializer,
            404: {'description': 'Payment not found'}
        },
        tags=['Payments']
    )
    def get(self, request, payment_id):
        """Get payment details"""
        payment = payment_get_by_id(payment_id=payment_id)
        serializer = PaymentDetailOutputSerializer(payment)
        return Response(
            {
                'payment': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='payments_update',
        summary='Update a payment',
        description='Update an existing payment. Staff/admin only.',
        request=PaymentUpdateInputSerializer,
        responses={
            200: PaymentDetailOutputSerializer,
            400: {'description': 'Validation error'},
            404: {'description': 'Payment not found'}
        },
        tags=['Payments']
    )
    def put(self, request, payment_id):
        """Update a payment"""
        serializer = PaymentUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = payment_update(payment_id=payment_id, **serializer.validated_data)
        
        output_serializer = PaymentDetailOutputSerializer(payment)
        return Response(
            {
                'message': 'Payment updated successfully.',
                'payment': output_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id='payments_delete',
        summary='Delete a payment',
        description='Delete a payment. Staff/admin only.',
        responses={
            200: {'description': 'Payment deleted successfully', 'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}},
            404: {'description': 'Payment not found'}
        },
        tags=['Payments']
    )
    def delete(self, request, payment_id):
        """Delete a payment"""
        payment_delete(payment_id=payment_id)
        return Response(
            {
                'message': 'Payment deleted successfully.'
            },
            status=status.HTTP_200_OK
        )

