from rest_framework import serializers
from .models import Link
from datetime import timedelta

class LinkSerializer(serializers.ModelSerializer):
    clicks_last_hour = serializers.SerializerMethodField()
    clicks_last_day = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['short_code', 'created_at', 'click_count', 'created_by']

    def get_clicks_last_hour(self, obj):
        from django.utils import timezone
        one_hour_ago = timezone.now() - timedelta(hours=1)
        return obj.click_logs.filter(timestamp__gte=one_hour_ago).count()

    def get_clicks_last_day(self, obj):
        from django.utils import timezone
        one_day_ago = timezone.now() - timedelta(days=1)
        return obj.click_logs.filter(timestamp__gte=one_day_ago).count()