from django.conf import settings
from django.db import models


class OfficerStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)

    last_lat = models.FloatField(null=True, blank=True)
    last_lng = models.FloatField(null=True, blank=True)
    last_accuracy = models.FloatField(null=True, blank=True)

    last_seen = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} status"
