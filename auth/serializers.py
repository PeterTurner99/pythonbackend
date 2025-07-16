from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "max_bookings_at_once"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.max_bookings_at_once = validated_data.get(
            "max_bookings_at_once", instance.max_bookings_at_once
        )
        instance.save()
        return instance
