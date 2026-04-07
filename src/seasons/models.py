from django.db import models

# Create your models here.

class Driver(models.Model):
    name = models.CharField(max_length=30)

    def find_competitors(self):
        return Competitor.objects.filter(driver=self).order_by('-season__year')

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
        return self.event_name






