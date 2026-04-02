from django.contrib.auth import get_user_model
from django.test import TestCase

from incidents.models import Incident
from incidents.services import assign_incident_to_officer


class IncidentServicesTests(TestCase):
    def test_assign_incident_to_selected_officer(self):
        user_model = get_user_model()
        officer = user_model.objects.create_user(
            username="officer1",
            password="test1234",
            role=user_model.Role.OFFICER,
        )
        incident = Incident.objects.create(lat=41.3, lng=69.2, status=Incident.Status.NEW)

        assigned = assign_incident_to_officer(incident, officer)
        incident.refresh_from_db()

        self.assertEqual(assigned.id, officer.id)
        self.assertEqual(incident.assigned_officer_id, officer.id)
        self.assertEqual(incident.status, Incident.Status.ASSIGNED)

    def test_assign_incident_to_non_officer_raises(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_user(
            username="admin1",
            password="test1234",
            role=user_model.Role.ADMIN,
        )
        incident = Incident.objects.create(lat=41.3, lng=69.2, status=Incident.Status.NEW)

        with self.assertRaisesMessage(ValueError, "Selected user is not OFFICER"):
            assign_incident_to_officer(incident, admin_user)
