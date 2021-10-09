import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventAdminForm
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Natan"

    month = str(month).capitalize()
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )
    # get current year
    now = datetime.now()
    c_year = now.year
    # get current time
    time = now.strftime('%H:%M:%S')
    return render(request,
                  'events/home.html',
                  {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "now": now,
                      "current_year": c_year,
                      "time": time,
                  })


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    # event_list = Event.objects.all().order_by('-name')
    # event_list = Event.objects.all()  # all the data from event model
    return render(request,
                  'events/event_list.html',
                  {"event_list": event_list})


def add_venue(request):
    submitted = False

    if request.method == "POST":
        if request.user.is_superuser:
            form = EventAdminForm(request.POST)
        # if it a post req so take all the post info and data
        # and pass it to Venue form
        else:
            form = VenueForm(request.POST)
        if form.is_valid():  # only if valid
            venue = form.save(commit=False)  # dont save it now
            venue.owner = request.user.id  # logged in user
            form.save()  # save to DB
            # redirct to some place and change submitted -> True
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventAdminForm(request.POST)
        else:
            form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'events/add_venue.html',
                  {'form': form, 'submitted': submitted})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('?')  # order in random way
    venue_list = Venue.objects.all()
    # set up pagination
    p = Paginator(Venue.objects.all(),
                  2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    pages_num = "a" * venues.paginator.num_pages

    return render(request,
                  'events/venues.html',
                  {"venue_list": venue_list, "venues": venues, "pages_num": pages_num})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request,
                  'events/show_venue.html',
                  {"venue": venue})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        events = Event.objects.filter(name__contains=searched)
        return render(request,
                      'events/search_venues.html',
                      {'searched': searched, 'venues': venues, 'events': events})
    else:
        return render(request,
                      'events/search_venues.html',
                      {})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    # if we made a post(submit form) req or just  get req
    # instance take venue obj and fill all the fields  of the form
    form = VenueForm(request.POST or None,
                     instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request,
                  'events/update_venue.html',
                  {"venue": venue, "form": form})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:  # if is user user -> admin
            form = EventAdminForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')

        # if it a post req so take all the post info and data
        # and pass it to Venue form
        else:
           form = EventForm(request.POST)
           if form.is_valid():  # only if valid
                # form.save()  # save to DB
                event = form.save(commit=False)
                event.manger = request.user
                event.save()
                # redirct to some place and change submitted -> True
                return HttpResponseRedirect('/add_event?submitted=True')
    else:  # get request
        if request.user.is_superuser:
            form = EventAdminForm
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'events/add_event.html',
                  {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventAdminForm(request.POST or None,instance=event)
    else:
            form = EventForm(request.POST or None,
                         instance=event)
    # if we made a post(submit form) req or just  get req
    # instance take venue obj and fill all the fields  of the form

    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request,
                  'events/update_event.html',
                  {"event": event, "form": form})


# Delete Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manger == request.user:
        event.delete()
        messages.success(request,("Event Deleted"))
        return redirect('list-events')

    else:
        messages.success(request,("you are not authorized to delete this event"))
        return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


# export and generate txt file of the venues
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment';
    'filename=venue.txt'

    # designate the model
    venues = Venue.objects.all()
    lines = []  # create empty list
    # loop thru and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zip_code}\n{venue.email_address}\n{venue.web}\n\n')

    # lines = ["This is a new line 1\n",
    #          "This is a new line 2\n",
    #          "This is a new line 3\n"
    #          "This is a new line 4\n"
    #          "This is a new line 5\n"
    #          "Natan wrote this\n"
    #          ]
    response.writelines(lines)
    return response


# generate csv file from venues
def venue_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="venues.csv"'},
    )
    # response = HttpResponse(content_type="text/csv")
    # response['Content-Disposition'] = 'attachment';'filename=venue.csv'
    # create csv writer
    writer = csv.writer(response)
    # designate the model
    venues = Venue.objects.all()
    # create columns headings to the csv file
    writer.writerow(['Venue name', "Address", "Zip Code", "Phone", "Web", "Email"])

    # loop thru and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.zip_code, venue.email_address, venue.web])

    return response


# Outputting PDFs with
def venue_pdf(request):
    venues = Venue.objects.all()

    # create bytes-stream buffer
    _buffer = io.BytesIO()
    # create canvas
    _canvas = canvas.Canvas(_buffer,
                            pagesize=letter,
                            bottomup=0)
    # create txt obj

    txtObj = _canvas.beginText(inch,
                               inch)
    txtObj.setFont("Helvetica",
                   14)

    # add some text

    # lines =["this is line 1","this is line 2","this is line 3"]
    lines = []  # create empty list
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.email_address)
        lines.append("====================")

    for line in lines:
        txtObj.textLine(line)

    _canvas.drawText(txtObj)
    _canvas.showPage()
    _canvas.save()
    _buffer.seek(0)

    return FileResponse(_buffer,
                        as_attachment=True,
                        filename="venue.pdf")
