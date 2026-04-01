from django.db import models
from django.conf import settings


class Incident(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "Yangi"
        ASSIGNED = "ASSIGNED", "Biriktirildi"
        ACCEPTED = "ACCEPTED", "Qabul qilindi"
        ARRIVED = "ARRIVED", "Yetib keldi"
        DONE = "DONE", "Bajarildi"
        CLOSED = "CLOSED", "Yopildi"
        CANCELED = "CANCELED", "Bekor qilindi"

    # ===== Vizov ma'lumotlari =====
    title = models.CharField(max_length=120, default="Vizov")
    details = models.TextField(blank=True, default="")

    # ===== Jabrlanuvchi =====
    victim_first_name = models.CharField(max_length=80, blank=True, default="")
    victim_last_name = models.CharField(max_length=80, blank=True, default="")
    caller_phone = models.CharField(max_length=40, blank=True, default="")

    # ===== Manzil =====
    address_text = models.CharField(max_length=255, blank=True, default="")
    lat = models.FloatField()
    lng = models.FloatField()

    # ===== Status =====
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    # ===== Ofitser =====
    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_incidents"
    )

    # ===== Kim yaratdi =====
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_incidents"
    )

    # ===== VAQTLAR =====
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # ===== SLA hisoblash =====
    def sla_seconds(self):
        if self.accepted_at and self.arrived_at:
            return (self.arrived_at - self.accepted_at).total_seconds()
        return None

    def __str__(self):
        return f"Incident #{self.id} - {self.status}"

    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
