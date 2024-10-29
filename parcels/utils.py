import random
import string
import time
from django.core.cache import cache
from django.db import transaction
from .models import TrackingNumber


def generate_tracking_number(prefix=''):
    """
    Generates a unique parcels number using a combination of timestamp and random characters.
    Includes retry logic and distributed locking for concurrent safety.
    """
    LOCK_TIMEOUT = 2  # seconds
    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):
        # Generate timestamp component (base36 encoded)
        timestamp = hex(int(time.time() * 1000))[2:].upper()

        # Generate random component (4 characters)
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        # Combine components
        tracking_number = f"{prefix}{timestamp[-6:]}{random_chars}"

        # Ensure it fits the regex pattern ^[A-Z0-9]{1,16}$
        tracking_number = tracking_number[:16]

        # Try to acquire a distributed lock
        lock_key = f"tracking_lock:{tracking_number}"
        if cache.add(lock_key, "locked", timeout=LOCK_TIMEOUT):
            try:
                # Check if parcels number exists
                if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                    return tracking_number
            finally:
                cache.delete(lock_key)

        time.sleep(0.1)  # Small delay before retry

    raise Exception("Failed to generate unique parcels number after maximum retries")
