from rest_framework import serializers
from .models import TrackingNumber
from django.utils import timezone
import re
import uuid


# Predefined set of ISO 3166-1 alpha-2 country codes
VALID_COUNTRY_CODES = {
    'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU',
    'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL',
    'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC',
    'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV',
    'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG',
    'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE',
    'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GT', 'GU', 'GW',
    'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO',
    'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM',
    'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
    'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML',
    'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY',
    'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ',
    'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PT', 'PW',
    'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG',
    'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX',
    'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO',
    'TR', 'TT', 'TV', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE',
    'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
}


class TrackingNumberRequestSerializer(serializers.Serializer):
    origin_country_id = serializers.CharField(max_length=2)
    destination_country_id = serializers.CharField(max_length=2)
    weight = serializers.DecimalField(max_digits=10, decimal_places=3)
    order_created_at = serializers.DateTimeField()
    customer_id = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=255)
    customer_slug = serializers.CharField(max_length=255)

    def validate_origin_country_id(self, value):
        if not re.match(r'^[A-Z]{2}$', value) or value not in VALID_COUNTRY_CODES:
            raise serializers.ValidationError("Origin country ID must be a valid ISO 3166-1 alpha-2 code (e.g., 'MY').")
        return value

    def validate_destination_country_id(self, value):
        if not re.match(r'^[A-Z]{2}$', value) or value not in VALID_COUNTRY_CODES:
            raise serializers.ValidationError("Destination country ID must be a valid ISO 3166-1 alpha-2 code (e.g., 'ID').")
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        return value

    def validate_customer_id(self, value):
        try:
            uuid.UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Customer ID must be a valid UUID.")
        return value

    def validate_customer_slug(self, value):
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', value):
            raise serializers.ValidationError("Customer slug must be in kebab-case (e.g., 'redbox-logistics').")
        return value


class TrackingNumberResponseSerializer(serializers.ModelSerializer):
    order_created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')

    class Meta:
        model = TrackingNumber
        fields = ['tracking_number', 'order_created_at', 'created_at']


class TrackingNumberSerializer(serializers.ModelSerializer):
    order_created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')

    class Meta:
        model = TrackingNumber
        fields = '__all__'
