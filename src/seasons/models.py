from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=30)

    def find_competitors(self):
        return Competitor.objects.filter(driver=self).order_by('-season__year')

    def get_all_events(self):
        competitors = Competitor.objects.filter(driver=self).prefetch_related('event_set')
        events = []
        for competitor in competitors:
            events += competitor.event_set.all()
        return events

    def get_all_season_placements(self):
        competitors = self.find_competitors()
        return competitors.values_list('season_placement', flat=True)

    def get_average_event_points(self):
        competitors = self.find_competitors()
        points = competitors.values_list('average_points', flat=True)
        return sum(points) / len(points)

    def get_average_doty_placement(self):
        placements = self.get_all_season_placements()
        return sum(placements) / len(placements)

    def get_best_event(self):
        competitors = Competitor.objects.filter(driver=self).prefetch_related('event_set')
        best_points = 0
        best_event = "temp"
        for competitor in competitors:
            best = competitor.get_best_event().doty_points
            if best > best_points:
                best_points = best
                best_event = competitor.get_best_event().event_name + " " + str(competitor.season)
        return best_event, best_points

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

    def get_best_event(self):
        return Event.objects.filter(competitor=self).order_by('-doty_points').first()

    def __str__(self):
        return self.driver.name + ' ' +str(self.season.year)

class Event(models.Model):
    event_name = models.CharField(max_length=3)
    doty_points = models.FloatField(default=0.0)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name






