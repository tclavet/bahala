from django.shortcuts import render, redirect
import datetime
from booking.models import OpenDate, Booking
from booking.forms import DateForm
from django.contrib import messages
from django import forms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def booking(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            new_booking = Booking()
            new_booking.date = form.cleaned_data['date']
            new_booking.seats = form.cleaned_data['seats']
            new_booking.info = form.cleaned_data['info']
            new_booking.phone_number = form.cleaned_data['phone_number']

            opendate = OpenDate.objects.get(date = form.cleaned_data['date'])
            remaining = opendate.seats - int(form.cleaned_data['seats'])
            if remaining == 0:
                opendate.seats -= int(form.cleaned_data['seats'])
                opendate.is_booked = 1
            elif remaining == 1:
                opendate.seats = 0
                opendate.is_booked = 1
            else:
                opendate.seats = remaining
            opendate.save()

            new_booking.save()
            request.session['form-submitted'] = True
            try:
                send_mail(
                    subject = "Booking for " + new_booking.date.strftime('%Y-%m-%d'),
                    message = "A booking for " + new_booking.seats + " seats on " + new_booking.date.strftime('%Y-%m-%d') + " was made.",
                    from_email = "booking@restaurant.com",
                    recipient_list = ['clavethom@gmail.com']
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('confirmation')
    else:
        form = DateForm(initial = {'information' : 'Please enter all the information necessary as explained above.\nAny incomplete booking or without enough information will be automatically cancelled.'})

    dates = OpenDate \
            .objects \
            .filter(date__gte=datetime.date.today()) \
            .filter(is_booked = False)

    if dates:
        empty = 0
    else:
        empty = 1

    return render(request, 'booking/booking.html', dict(form=form, empty=empty))

def confirmation(request):
    if not request.session.get('form-submitted', False):
        return redirect('booking')
    else:
        request.session['form-submitted'] = False
        return render(request, 'booking/confirmation.html')
