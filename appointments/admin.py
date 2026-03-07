from django.contrib import admin
from .models import Profile, AvailabilitySlot, Appointment

admin.site.register(Profile)
admin.site.register(AvailabilitySlot)
admin.site.register(Appointment)