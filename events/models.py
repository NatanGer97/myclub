from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Venue(models.Model):
    name = models.CharField('Venue name',
                            max_length=120)
    address = models.CharField('Venue Address',
                               max_length=300)
    zip_code = models.CharField('Zip Code',
                                max_length=15,
                                blank=True)
    phone = models.CharField('Contact Phone',
                             max_length=25,
                             blank=True)
    web = models.URLField('Website Address',
                          blank=True)
    email_address = models.EmailField('Email Address',
                                      blank=True)
    owner = models.IntegerField("Venue Owner",blank=False,default=1,editable=False) # in default admin is the owner

    # override str method
    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField("Event Name",
                            max_length=120)
    venue = models.ForeignKey(Venue,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
    event_date = models.DateTimeField('Event Date')
    # venue = models.CharField(max_length=120)
    manger = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)
    # manger = models.CharField(max_length=60)
    attendees = models.ManyToManyField(MyClubUser,
                                       blank=True)
    description = models.TextField(blank=True)  # blank = True -> empty text field

    # override str method
    def __str__(self):
        return self.name
