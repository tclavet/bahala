from django.db import models
from django.urls import reverse
import datetime

class OpenDate(models.Model):
    date = models.DateField(default = datetime.datetime.today())
    seats = models.PositiveSmallIntegerField(unique_for_date='date')
    is_booked = models.BooleanField(default = False)

    def __str__(self):
        return self.date.strftime("%d-%m-%Y")

    def save(self, *args, **kwargs):
        super(OpenDate, self).save(*args, **kwargs)

class Booking(models.Model):
    date = models.DateField(default = datetime.datetime.today())
    booking_time = models.DateTimeField(auto_now = True)
    seats = models.PositiveSmallIntegerField(unique_for_date='booking_time')
    info = models.TextField(default = "info")
    phone_number = models.TextField(max_length=17, default="+330000000000")

    def __str__(self):
        booking = "Booked at " \
                    + self.booking_time.strftime("%d-%m-%Y %H:%M") \
                    + " for the day " \
                    + self.date.strftime("%d-%m-%Y")
        return booking

    def save(self, *args, **kwargs):
        super(Booking, self).save(*args, **kwargs)
