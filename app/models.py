from django.db import models
from django.core.exceptions import ValidationError
from app.querysets import MatchQuerySet
from datetime import timedelta
from d2lbetting.settings import TRAIN_PERIOD, BET_AMOUNT, HOUSE_RESERVE


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
        get_latest_by = 'datetime'

    def payout_factor(self, team):
        """
        Multiply base bet to get profit.
        """
        if self.team1 == team:
            return self.team2_odds / self.team1_odds
        elif self.team2 == team:
            return self.team1_odds / self.team2_odds
        else:
            return 0

    def team1_bet_factor(self):
        winrate = self.team1.past_winrate(self.datetime)
        mean_odds = float(self.team1.past_mean_odds(self.datetime))
        payout_factor = float(self.payout_factor(self.team1))
        # ALGO
        bet_factor = payout_factor * float(self.team2_odds) * winrate / mean_odds
        return bet_factor

    def team1_netgain_factor(self):
        return self.team1_bet_factor() - self.team2_bet_factor()

    def team2_bet_factor(self):
        winrate = self.team2.past_winrate(self.datetime)
        mean_odds = float(self.team2.past_mean_odds(self.datetime))
        payout_factor = float(self.payout_factor(self.team2))
        # ALGO
        bet_factor = payout_factor * float(self.team1_odds) * winrate / mean_odds
        return bet_factor

    def team2_netgain_factor(self):
        return self.team2_bet_factor() - self.team1_bet_factor()

    def has_team(self, team):
        if self.team1 == team or self.team2 == team:
            return True
        else:
            return False

    def auto_bet(self):
        if self.team1_bet_factor() > self.team2_bet_factor():
            return self.bet(self.team1)
        else:
            return self.bet(self.team2)

    def bet(self, team, console=True):
        if self.winner == team:
            outcome = self.payout_factor(team) * BET_AMOUNT
            # if console:
        else:
            outcome = -1 * BET_AMOUNT
        return outcome


class Team(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def matches_played(self, queryset=Match.objects.valid()):
        matches = queryset.filter(
            models.Q(team1__name=self.name) | models.Q(team2__name=self.name)
        )
        return matches

    def matches_won(self, queryset=Match.objects.valid()):
        matches = queryset.filter(
            models.Q(winner__name=self.name)
        )
        return matches

    def winrate(self, queryset=Match.objects.valid()):
        won = self.matches_won(queryset).count()
        played = self.matches_played(queryset).count()
        score = 1.0 * won / played
        return score

    def past_winrate(self, datetime):
        queryset = self.past_queryset(datetime)
        return self.winrate(queryset)

    def mean_odds(self, queryset=Match.objects.valid()):
        total_odds = 0
        matches = self.matches_played(queryset)
        for match in matches:
            if match.team1 == self:
                total_odds += match.team1_odds
            elif match.team2 == self:
                total_odds += match.team2_odds
        mean_odds = total_odds / matches.count()
        return mean_odds

    def past_mean_odds(self, datetime):
        queryset = self.past_queryset(datetime)
        return self.mean_odds(queryset)

    def past_queryset(self, datetime):
        start = datetime - timedelta(days=TRAIN_PERIOD)
        queryset = Match.objects.time_period(start, datetime)
        return queryset
