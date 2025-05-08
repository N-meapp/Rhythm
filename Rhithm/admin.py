from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BookingRequest)
admin.site.register(Register)

# @admin.register(BookingRequest)
# class BookingRequestAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'event_date', 'event_type', 'status', 'created_at')
#     list_filter = ('status', 'event_date')
#     search_fields = ('name', 'email', 'event_type', 'location')
#     ordering = ('-created_at',)
