from django.urls import path

from .views import NginxLogsView

urlpatterns = [
    path('nginx_logs/', NginxLogsView.as_view(), name='nginx_logs')
]
