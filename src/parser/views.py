from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .filters import NginxLogFilter
from .models import NginxLog
from .serializers import NginxLogSerializer


# Create your views here.
class NginxLogsView(ListAPIView):
    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NginxLogFilter
    search_fields = NginxLog.SEARCHABLE_FIELDS
    ordering_fields = ['id', 'response_code', 'response_size']