from django.contrib import admin

from .models import NginxLog


# Register your models here.
class NginxLogAdmin(admin.ModelAdmin):
    list_display = NginxLog.DISPLAY_FIELDS
    search_fields = NginxLog.SEARCHABLE_FIELDS
    list_filter = NginxLog.FILTER_FIELDS

admin.site.register(NginxLog, NginxLogAdmin)