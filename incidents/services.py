from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Incident

class OfficerAcceptIncident(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        inc = get_object_or_404(Incident, pk=pk, assigned_officer=request.user)
        if inc.status not in ("ASSIGNED","NEW"):
            return Response({"detail":"Bad status"}, status=400)
        inc.status = "ACCEPTED"
        inc.accepted_at = timezone.now()
        inc.save()
        return Response({"ok": True})

class OfficerArriveIncident(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        inc = get_object_or_404(Incident, pk=pk, assigned_officer=request.user)
        if inc.status != "ACCEPTED":
            return Response({"detail":"Bad status"}, status=400)
        inc.status = "ARRIVED"
        inc.arrived_at = timezone.now()
        inc.save()
        return Response({"ok": True, "sla_seconds": inc.sla_seconds()})
import math
from datetime import timedelta
from django.utils import timezone
from accounts.models import User
from tracking.models import OfficerStatus

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    d1 = math.radians(lat2 - lat1)
    d2 = math.radians(lon2 - lon1)
    a = math.sin(d1/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(d2/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def pick_nearest_officer(lat, lng, minutes_alive=10):
    alive_after = timezone.now() - timedelta(minutes=minutes_alive)

    qs = OfficerStatus.objects.select_related("user").filter(
        is_online=True,
        last_seen__gte=alive_after,
        user__role=User.Role.OFFICER,
    )

    best_user = None
    best_dist = None

    for st in qs:
        if st.last_lat is None or st.last_lng is None:
            continue
        d = haversine_km(lat, lng, float(st.last_lat), float(st.last_lng))
        if best_dist is None or d < best_dist:
            best_dist = d
            best_user = st.user

    return best_user, best_dist
from math import radians, sin, cos, sqrt, atan2

from tracking.models import OfficerStatus


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def assign_nearest_online_officer(incident):
    if incident.lat is None or incident.lng is None:
        return None

    qs = (
        OfficerStatus.objects
        .select_related("user")
        .filter(
            is_online=True,
            last_lat__isnull=False,
            last_lng__isnull=False,
            user__role=User.Role.OFFICER,
        )
    )

    best_status = None
    best_dist = None

    for st in qs:
        d = _haversine_km(
            float(incident.lat),
            float(incident.lng),
            float(st.last_lat),
            float(st.last_lng),
        )
        if best_dist is None or d < best_dist:
            best_dist = d
            best_status = st

    if best_status:
        incident.assigned_officer = best_status.user
        incident.status = "ASSIGNED"
        incident.save(update_fields=["assigned_officer", "status"])
        return best_status.user

    return None


