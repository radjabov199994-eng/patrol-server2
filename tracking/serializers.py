from rest_framework import serializers

from .models import OfficerStatus


class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accuracy = serializers.FloatField(required=False)


class OfficerStatusSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    position = serializers.CharField(source="user.position", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if not obj.user.photo:
            return ""
        url = obj.user.photo.url
        return request.build_absolute_uri(url) if request else url

    class Meta:
        model = OfficerStatus
        fields = [
            "id",
            "user",
            "username",
            "first_name",
            "last_name",
            "position",
            "phone",
            "photo_url",
            "last_lat",
            "last_lng",
            "last_accuracy",
            "last_seen",
            "is_online",
            "updated_at",
        ]
