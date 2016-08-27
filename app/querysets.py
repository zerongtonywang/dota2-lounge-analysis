from django.db import models


class MatchMixin:
    def include_team(self, team_name):
        return self.filter(
            models.Q(team1__name=team_name) | models.Q(team2__name=team_name)
        )

    def winning_team(self, team_name):
        return self.filter(
            models.Q(winner__name=team_name)
        )

    def from_past(self, time_period):
        pass


class MatchQuerySet(models.query.QuerySet, MatchMixin):
    pass
