from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=30)

    def get_all_related_competitors(self, year_span = 100):
        min_year = int(Season.objects.order_by('-year').values_list('year', flat=True).first()) - year_span
        return Competitor.objects.filter(driver=self, season__year__gt=min_year).order_by('-season__year')

    def get_all_related_events(self, year_span = 100):
        competitors = self.get_all_related_competitors(year_span)
        return Event.objects.filter(competitor__in=competitors)

    def __str__(self):
        return self.name

class Season(models.Model):
    year = models.CharField(max_length=4)
    total_event_count = models.IntegerField(default=0)
    season_is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.year

class Competitor(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    season_placement = models.IntegerField()
    season_points = models.FloatField(default=0)
    average_points = models.FloatField(default=0)

    def __str__(self):
        return self.driver.name + ' ' +str(self.season.year)

class Event(models.Model):
    event_name = models.CharField(max_length=3)
    doty_points = models.FloatField(default=0.0)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name + ' ' + str(self.competitor.season)






