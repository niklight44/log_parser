from rest_framework import serializers

from .models import NginxLog


class NginxLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NginxLog
        fields = '__all__'

