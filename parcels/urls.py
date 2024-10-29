from django.urls import path
from .views import NextTrackingNumberView, ParcelDeleteView, ParcelListView

urlpatterns = [
    path('next-tracking-number/', NextTrackingNumberView.as_view(), name='next-tracking-number'),
    path('parcels/list/', ParcelListView.as_view(), name='parcel-list'),
    path('parcels/<str:pk>/', ParcelDeleteView.as_view(), name='parcel-delete'),
]
