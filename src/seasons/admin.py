from django.contrib import admin

from .models import Season, Competitor, Event, Driver


# Register your models here.

class CompetitorInline(admin.TabularInline):
    model = Competitor
    extra = 0

class EventInline(admin.TabularInline):
    model = Event
    extra = 0

class CompetitorAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    search_fields = ["driver__name", "season__year"]
    ordering = ["driver__name", "season__year"]


class SeasonAdmin(admin.ModelAdmin):
    inlines = [CompetitorInline]
    search_fields = ["year"]

class DriverAdmin(admin.ModelAdmin):
    search_fields = ["name"]

admin.site.register(Season, SeasonAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Event)
admin.site.register(Driver, DriverAdmin)

