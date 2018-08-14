from django.contrib import admin
from booking import models

# Register your models here.
class OpenDateAdmin(admin.ModelAdmin):
    model = models.OpenDate

class BookingAdmin(admin.ModelAdmin):
    model = models.Booking
    readonly_fields = ('booking_time',)

admin.site.register(models.OpenDate, OpenDateAdmin)
admin.site.register(models.Booking, BookingAdmin)
