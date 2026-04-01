from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .models import OfficerStatus
from .serializers import LocationSerializer


class OfficerLocationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):   # 👈 BU QATOR

        # Faqat OFFICER lokatsiya yuborsin
        if getattr(request.user, "role", None) != User.Role.OFFICER:
            return Response({"detail": "Only officers can send location."}, status=403)

        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lat = serializer.validated_data["latitude"]
        lng = serializer.validated_data["longitude"]
        acc = serializer.validated_data.get("accuracy")

        status_obj, _ = OfficerStatus.objects.get_or_create(user=request.user)
        status_obj.last_lat = lat
        status_obj.last_lng = lng
        status_obj.last_accuracy = acc
        status_obj.last_seen = timezone.now()
        status_obj.is_online = True
        status_obj.save()

        return Response({"ok": True})

from rest_framework.permissions import IsAdminUser
from .serializers import OfficerStatusSerializer


class AdminOfficersListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        qs = OfficerStatus.objects.select_related("user").all().order_by("-updated_at")
        data = OfficerStatusSerializer(qs, many=True, context={"request": request}).data
        return Response(data)
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def admin_dashboard(request):
    return render(request, "dashboard/map.html")


    



