from django.db import models


# Create your models here.
class NginxLog(models.Model):
    ip = models.CharField(max_length=256)
    date = models.DateField()
    method = models.CharField()
    request_URI = models.CharField()
    response_code = models.IntegerField()
    response_size = models.IntegerField()
    SEARCHABLE_FIELDS = ['id', 'date', 'request_URI']
    FILTER_FIELDS = ['id', 'date', 'method', 'response_size']
    DISPLAY_FIELDS = ['id', 'date', 'method', 'request_URI', 'response_code', 'response_size']
