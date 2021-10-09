from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event

# Register your models here.

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone',"email_address")
    ordering = ('name',)
    search_fields = ('name','address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','venue'),'event_date','description','manger')
    list_display = ('name','event_date')
    list_filter = ('event_date','venue')
    ordering = ('-event_date',)
