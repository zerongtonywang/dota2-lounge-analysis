from django.db import models
from app.querysets import MatchQuerySet


class Team(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(
        Team,
        related_name='match_as_team1'
    )
    team1_odds = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    team2 = models.ForeignKey(
        Team,
        related_name='match_as_team2'
    )
    team2_odds = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    winner = models.ForeignKey(
        Team,
        related_name='match_as_winner',
        null=True,
        blank=True
    )

    datetime = models.DateTimeField()
    finished = models.BooleanField(default=True)
    bestof = models.IntegerField(default=1)
    event = models.CharField(max_length=40, null=True, blank=True)

    valid = models.BooleanField()

    objects = MatchQuerySet.as_manager()

    def __str__(self):
        return 'Match {}'.format(self.id)

    def save(self, **kwargs):
        self.valid = self.is_valid()
        super().save(**kwargs)

    def is_valid(self):
        condidtions = [
            # self.bestof > 0,
            self.finished,
            self.winner,
            self.team1_odds,
            self.team2_odds
        ]
        return all(condidtions)

    class Meta:
        verbose_name_plural = 'Matches'
