from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status', 'severity')
    search_fields = ('doctor__user__email', 'patient__email', 'status', 'severity')
    list_filter = ('status', 'severity', 'date')

admin.site.register(Appointment, AppointmentAdmin)
