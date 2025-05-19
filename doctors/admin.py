from django.contrib import admin
from .models import DoctorProfile, DoctorAvailability
from .models_rating import DoctorRating
class DoctorRatingAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    search_fields = ('doctor__user__email', 'patient__email')
    list_filter = ('rating',)

admin.site.register(DoctorRating, DoctorRatingAdmin)

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'years_of_experience', 'is_verified', 'certificate_document')
    search_fields = ('user__email', 'specialty')
    list_filter = ('specialty', 'is_verified')
    actions = ['approve_doctor', 'reject_doctor']

    def approve_doctor(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} doctor(s) approved.")
    approve_doctor.short_description = "Approve selected doctors"

    def reject_doctor(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} doctor(s) rejected.")
    reject_doctor.short_description = "Reject selected doctors"

admin.site.register(DoctorProfile, DoctorProfileAdmin)

class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'slot_duration_minutes')
    list_filter = ('doctor', 'day_of_week')

admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)
