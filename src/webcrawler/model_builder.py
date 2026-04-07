from seasons.models import Event, Competitor, Season, Driver


class ModelBuilder:

    #| event_1 | ... | event_n |
    @staticmethod
    def build_events(event_data: list):
        event_list = []
        event_count = 1
        for event in event_data:
            event_obj: Event = Event()
            event_obj.event = "M" + event_count
            event_obj.doty_points = event
            event_list.append(event)
            event_count += 1
        return event_list

    #|rank|total_points|avg_points|
    @staticmethod
    def build_competitor(competitor_data: list):
        competitor = Competitor()
        competitor.competitor_name = competitor_data[0]
        competitor.season_points = competitor_data[1]
        competitor.doty_points = competitor_data[2]
        return competitor

    @staticmethod
    def build_season(season_data: list):
        season = Season()
        return season

    @staticmethod
    def build_driver(driver_data: list):
        driver = Driver()
        return driver