from django.contrib import admin
from .models import MeterReadings


class MeterReadingsAdmin(admin.ModelAdmin):
    list_display = ('cold', 'hot', 'publish', 'user',)


admin.site.register(MeterReadings, MeterReadingsAdmin)
