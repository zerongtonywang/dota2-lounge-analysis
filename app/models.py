from django.db import models
from app.querysets import MatchQuerySet


class Match(models.Model):
    team1 = models.ForeignKey(
        'app.Team',
        related_name='match_as_team1'
    )
    team1_odds = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    team2 = models.ForeignKey(
        'app.Team',
        related_name='match_as_team2'
    )
    team2_odds = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    winner = models.ForeignKey(
        'app.Team',
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


class Team(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def get_matches_played(self, queryset=Match.objects.valid_matches()):
        matches = queryset.filter(
            models.Q(team1__name=self.name) | models.Q(team2__name=self.name)
        )
        return matches

    def get_matches_won(self, queryset=Match.objects.valid_matches()):
        matches = queryset.filter(
            models.Q(winner__name=self.name)
        )
        return matches

    def get_winrate(self, queryset=Match.objects.valid_matches()):
        won = self.get_matches_won(queryset).count()
        played = self.get_matches_played(queryset).count()
        score = 1.0 * won / played
        return score

    def get_mean_odds(self, queryset=Match.objects.valid_matches()):
        total_odds = 0
        matches = self.get_matches_played(queryset)
        for match in matches:
            if match.team1 == self:
                total_odds += match.team1_odds
            elif match.team2 == self:
                total_odds += match.team2_odds
        mean_odds = total_odds / matches.count()
        return mean_odds
