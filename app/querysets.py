from django.db import models


class MatchMixin:
    def valid(self):
        return self.filter(valid=True)

    def time_period(self, start_date, end_date):
        return self.filter(datetime__range=[start_date, end_date])


class MatchQuerySet(models.query.QuerySet, MatchMixin):
    pass
