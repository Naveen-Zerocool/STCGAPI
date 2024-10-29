from django.db import models
import uuid

class TrackingNumber(models.Model):
    tracking_number = models.CharField(primary_key=True, max_length=16, unique=True, db_index=True)
    origin_country_id = models.CharField(max_length=2)
    destination_country_id = models.CharField(max_length=2)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    order_created_at = models.DateTimeField()
    customer_id = models.UUIDField()
    customer_name = models.CharField(max_length=255)
    customer_slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['origin_country_id']),
            models.Index(fields=['destination_country_id']),
        ]
        ordering = ['-created_at']
