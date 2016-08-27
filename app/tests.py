from django.test import TestCase
from model_mommy import mommy

from d2lbetting.settings import BET_AMOUNT


class PayoutTests(TestCase):
    def setUp(self):
        self.team1 = mommy.make('Team')
        self.team2 = mommy.make('Team')

    def spawn_queryset(self, count=20):
        for i in range(count):
            mommy.make(
                'Match',
                team1=self.team1,
                team2=self.team2,
            )

    def test_bet_outcome_ok(self):
        match = mommy.make(
            'Match',
            team1=self.team1,
            team1_odds=0.80,
            team2=self.team2,
            team2_odds=0.20,
            winner=self.team1,
            valid=True
        )
        outcome = match.auto_bet()

        self.assertEqual(
            outcome,
            0.2 / 0.8 * BET_AMOUNT
        )
