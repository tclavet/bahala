from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
import datetime
from booking.models import OpenDate, Booking
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator
import re

def get_open_dates():
    try:
        dates = OpenDate \
            .objects \
            .filter(date__gte=datetime.date.today()) \
            .filter(is_booked = False)
        dates_list = list(dates.values_list('date', flat = True))
        dates_string = [date.strftime("%Y-%m-%d") for date in dates_list]
    except:
        dates_string = []
    return dates_string

class DateForm(forms.Form):
        date = forms.DateField(
            widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                            "dayViewHeaderFormat": "MMMM YYYY",
                                            #"enabledDates": get_open_dates()
                                            }))
        seats = forms.CharField(
            widget=forms.Select(
                attrs={"class": "form-control"},
                choices =  ((('2', '2'), ('3', '3'), (('4', '4'))))
                )
            )
        information = forms.CharField(
            widget=forms.Textarea(attrs={"class": "form-control"})
        )
        phone_number = forms.CharField(
            widget=forms.TextInput(attrs={"class": "form-control"})
        )

        class Meta:
            model = Booking

        def clean_date(self):
            date = self.cleaned_data['date']
            open_dates = OpenDate \
                    .objects \
                    .filter(date__gte=datetime.date.today()) \
                    .filter(is_booked = False)
            open_dates = list(open_dates.values_list('date', flat = True))
            if date not in open_dates:
                raise forms.ValidationError("This is not a valid date")
            return date

        def clean_phone_number(self):
            phone_number = self.cleaned_data['phone_number']
            if not re.match(r'^\+?1?\d{9,15}$', phone_number):
                raise forms.ValidationError("""Phone number must be entered in the format: '+33xxxxxxxxxx'.""")
            return phone_number

        def clean_seats(self):
            seats = self.cleaned_data['seats']
            try:
                date = OpenDate.objects.get(date = self.cleaned_data['date'])
            except:
                raise forms.ValidationError("Please enter a valid date first")
            if date.seats == 2 and int(seats) > 2:
                raise forms.ValidationError("Sorry, there is only " + str(date.seats) + " seats left for this date")
            return seats
