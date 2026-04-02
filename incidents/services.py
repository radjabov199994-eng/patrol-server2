from math import radians, sin, cos, sqrt, atan2

from accounts.models import User
from tracking.models import OfficerStatus


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


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
        return assign_incident_to_officer(incident, best_status.user)

    return None


def assign_incident_to_officer(incident, officer):
    if getattr(officer, "role", None) != User.Role.OFFICER:
        raise ValueError("Selected user is not OFFICER")

    incident.assigned_officer = officer
    incident.status = "ASSIGNED"
    incident.save(update_fields=["assigned_officer", "status"])
    return officer
