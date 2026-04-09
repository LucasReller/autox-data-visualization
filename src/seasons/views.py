
from datetime import datetime

from django.db.models.aggregates import Avg
from django.views import generic

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

class DriversListView(generic.ListView):
    template_name = "seasons/index.html"
    context_object_name = "seasons_list"

    def get_queryset(self):
        return Season.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DriversListView, self).get_context_data(**kwargs)
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

class DriverView(generic.DetailView):
    model = Driver
    template_name = "seasons/driver.html"
    context_object_name = "driver"

    def get_context_data(self, **kwargs):
        context = super(DriverView, self).get_context_data(**kwargs)
        context['lifetime_avg_points'] = Driver.get_all_related_competitors(self.object).aggregate(avg=Avg('average_points'))['avg']
        context['lifetime_avg_doty'] = Driver.get_all_related_competitors(self.object).aggregate(avg=Avg('season_placement'))['avg']
        context['lifetime_best_doty_placement'] = min(Driver.get_all_related_competitors(self.object).values_list('season_placement', flat=True))
        context['lifetime_best_doty_season'] = Driver.get_all_related_competitors(self.object).order_by('season_placement').values_list('season__year', flat=True).first()
        context['lifetime_best_event_points'] = Driver.get_all_related_events(self.object).order_by('-doty_points', '-competitor__season__year').first().doty_points
        context['lifetime_best_event'] = Driver.get_all_related_events(self.object).order_by('-doty_points', '-competitor__season__year').first().event_name
        context['lifetime_event_count'] = len(Driver.get_all_related_events(self.object))

        context['filtered_avg_points'] = Driver.get_all_related_competitors(self.object, 5).aggregate(avg=Avg('average_points'))['avg']
        context['filtered_avg_doty'] = Driver.get_all_related_competitors(self.object, 5).aggregate(avg=Avg('season_placement'))['avg']
        context['filtered_best_doty_placement'] = min(Driver.get_all_related_competitors(self.object, 5).values_list('season_placement', flat=True))
        context['filtered_best_doty_season'] = Driver.get_all_related_competitors(self.object, 5).order_by('season_placement').values_list('season__year', flat=True).first()
        context['filtered_best_event_points'] = Driver.get_all_related_events(self.object, 5).order_by('-doty_points', '-competitor__season__year').first().doty_points
        context['filtered_best_event'] = Driver.get_all_related_events(self.object, 5).order_by('-doty_points', '-competitor__season__year').first().event_name
        context['filtered_event_count'] = len(Driver.get_all_related_events(self.object, 5))
        return context

