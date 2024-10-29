from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import TrackingNumberRequestSerializer, TrackingNumberResponseSerializer, TrackingNumberSerializer
from .models import TrackingNumber
from .utils import generate_tracking_number
from django.views.generic import ListView, FormView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
import requests
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class NextTrackingNumberView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    if settings.DEBUG:
        authentication_classes.append(SessionAuthentication)

    def get(self, request):
        # Validate request parameters
        serializer = TrackingNumberRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Generate unique parcels number
                tracking_number = generate_tracking_number(
                    prefix=
                    f"{serializer.validated_data.get('origin_country_id')}-{serializer.validated_data.get('destination_country_id')}-"
                )

                # Create parcels number record
                tracking_record = TrackingNumber.objects.create(
                    tracking_number=tracking_number,
                    **serializer.validated_data
                )

                # Serialize response
                response_serializer = TrackingNumberResponseSerializer(tracking_record)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Failed to generate parcels number"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ParcelListView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    if settings.DEBUG:
        authentication_classes.append(SessionAuthentication)

    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        queryset = TrackingNumber.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(customer_name__icontains=search_query) |
                Q(origin_country_id__icontains=search_query) |
                Q(destination_country_id__icontains=search_query)
            )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        parcels = TrackingNumberSerializer(page, many=True).data
        return paginator.get_paginated_response({'parcels': parcels})


class ParcelDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    if settings.DEBUG:
        authentication_classes.append(SessionAuthentication)

    def delete(self, request, *args, **kwargs):
        tracking_number_id = kwargs.get('pk')
        try:
            tracking_number = TrackingNumber.objects.get(pk=tracking_number_id)
            tracking_number.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TrackingNumber.DoesNotExist:
            return Response({'error': 'Tracking number not found'}, status=status.HTTP_404_NOT_FOUND)
