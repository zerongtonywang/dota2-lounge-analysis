from django.db import models
from datetime import timedelta


class MatchMixin:
    def valid(self):
        return self.filter(valid=True)

    def time_period(self, start_date, end_date, train=False):
        if train:
            end_date -= timedelta(minutes=45)
        return self.filter(datetime__range=[start_date, end_date])


class MatchQuerySet(models.query.QuerySet, MatchMixin):
    pass
