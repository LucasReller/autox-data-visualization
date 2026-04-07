import sys
from datetime import datetime
from xmlrpc.client import DateTime

from django.shortcuts import get_object_or_404, render
from django.views import View, generic

from webcrawler.web_crawler import WebCrawler
from .models import Season, Driver, Competitor, Event


# Create your views here.

def check_for_new_data(year):
    if not Season.objects.filter(year=year).exists():
        crawler = WebCrawler(year)
        valid_crawler = crawler.read_html()
        if valid_crawler:
            event_count = crawler.get_season_event_count()
            Season.objects.create(year=year, total_event_count=event_count, season_is_complete=False)

    driver = None
    competitor = None

    for season in Season.objects.all():

        if not season.season_is_complete:
            crawler = WebCrawler(season.year)
            crawler.read_html()
            crawler.get_season_event_count()
            crawler.build_competitor_from_soup()

            competitor_index=0
            for competitor in crawler.competitor_list:
                if not Driver.objects.filter(name=competitor[1]).exists():
                    driver = Driver.objects.create(name=competitor[1])
                else:
                    driver = Driver.objects.get(name=competitor[1])
                if not Competitor.objects.filter(season=season, driver=driver).exists():
                    competitor = Competitor.objects.create(season=season, driver=driver, season_points=competitor[2], season_placement=competitor[0], average_points=competitor[3])
                else:
                    competitor = Competitor.objects.get(season=season, driver=driver)
                event_index = 1
                for event in crawler.event_list[competitor_index]:
                    if not Event.objects.filter(event_name="M"+str(event_index), competitor=competitor).exists():
                        if (not str(event) == '-') and (not float(event) == 0.0):
                            Event.objects.create(event_name="M"+str(event_index), competitor=competitor, doty_points=event)
                    event_index +=1
                competitor_index += 1
            if int(season.year) <= datetime.now().year:
                season.season_is_complete = True
                season.save()

class DriversView(generic.ListView):
    template_name = "seasons/index.html"
    context_object_name = "seasons_list"

    def get_queryset(self):
        return Season.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DriversView, self).get_context_data(**kwargs)
        context['seasons_list'] = Season.objects.all().order_by('-year')
        context['drivers_list'] = Driver.objects.all().order_by('name')
        return context

class CompetitorView(generic.DetailView):
    currentYear = str(datetime.now().year)
    check_for_new_data(currentYear)
    model = Competitor
    template_name = "seasons/competitor.html"
    context_object_name = "competitor"

    def get_queryset(self):
        return Competitor.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CompetitorView, self).get_context_data(**kwargs)
        context['events_list'] = Event.objects.filter(competitor=self.kwargs['pk'])
        return context

