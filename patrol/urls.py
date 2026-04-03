from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from patrol.views import home
from incidents.views import (
    daily_report_xlsx,
    incident_detail_page,
    CreateIncidentView,
    create_incident_form,
    IncidentListView,
    AssignIncidentView,
    officer_dashboard,
    OfficerIncidentStatusView,
    OfficerMyIncidentsView,
    MyProfileView,
    search_location,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tracking.views import AdminOfficersListView, admin_dashboard, OfficerLocationUpdateView

urlpatterns = [
    path("", home, name="home"),

    path("admin/", admin.site.urls),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", MyProfileView.as_view(), name="my_profile"),

    path("api/officer/location/", OfficerLocationUpdateView.as_view(), name="officer_location"),
    path("api/admin/officers/", AdminOfficersListView.as_view(), name="admin_officers"),

    path("accounts/", include("django.contrib.auth.urls")),

    path("dashboard/", admin_dashboard, name="dashboard"),
    path("officer/", officer_dashboard, name="officer_dashboard"),

    path("api/create-incident/", CreateIncidentView.as_view(), name="create_incident"),
    path("create-incident-form/", create_incident_form),
    path("api/incidents/", IncidentListView.as_view()),
    path("api/search-location/", search_location, name="search_location"),
    path("api/officer/my-incidents/", OfficerMyIncidentsView.as_view(), name="officer_my_incidents"),
    path("api/incidents/<int:pk>/assign/", AssignIncidentView.as_view()),
    path("api/officer/incidents/<int:pk>/status/", OfficerIncidentStatusView.as_view(), name="officer_incident_status"),

    path("reports/daily.xlsx", daily_report_xlsx, name="daily_report_xlsx"),
    path("dashboard/incidents/<int:pk>/", incident_detail_page, name="incident_detail_page"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)