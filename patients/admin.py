from django.contrib import admin
from .models import PatientProfile

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

admin.site.register(PatientProfile, PatientProfileAdmin)
