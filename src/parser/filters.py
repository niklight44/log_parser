from django_filters.rest_framework import FilterSet

from .models import NginxLog


class NginxLogFilter(FilterSet):
    class Meta:
        model = NginxLog
        fields = {
            'date': ['gt', 'lt'],
            'response_code': ['gt', 'lt'],
        }