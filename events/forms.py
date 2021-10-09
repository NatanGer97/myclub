from django import forms
from django.forms import ModelForm

from .models import Venue, Event


# create venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email.address')  # if we dont want all fields
        fields = "__all__"  # all the fields
        labels = {
            # 'name': "Venue name",
            # 'address': "Address",
            # 'zip_code': "Zip Code",
            # 'phone': "Phone",
            # 'web':"Web",
            # 'email_address': "Email"
            'name': "",
            'address': "",
            'zip_code': "",
            'phone': "",
            'web': "",
            'email_address': ""
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "name"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

        }


# name
# venue
# event_date
# manger
# description
# attendees

#Admin super user form
class EventAdminForm(ModelForm):
    class Meta:
        model = Event
        # fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email.address')  # if we dont want all fields
        fields = "__all__"  # all the fields
        labels = {
            # 'name': "Venue name",
            # 'address': "Address",
            # 'zip_code': "Zip Code",
            # 'phone': "Phone",
            # 'web':"Web",
            # 'email_address': "Email"
            'name': "",
            'venue': "Venue",
            'event_date': "DD-MM-YYYY HH:MM:SS",
            'manger': "Manger",
            'description': "",
            'attendees': "Attendees"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event Name"}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'event date'}),
            'manger': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manger'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),

        }

#user event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        # fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email.address')  # if we dont want all fields
         # fields = "__all__"  # all the fields
        fields = ('name','venue','event_date','attendees','description')

        labels = {
            # 'name': "Venue name",
            # 'address': "Address",
            # 'zip_code': "Zip Code",
            # 'phone': "Phone",
            # 'web':"Web",
            # 'email_address': "Email"
            'name': "",
            'venue': "Venue",
            'event_date': "DD-MM-YYYY HH:MM:SS",
            'description': "",
            'attendees': "Attendees"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event Name"}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'event date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),

        }
