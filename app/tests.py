from django.test import TestCase
from model_mommy import mommy

from d2lbetting.settings import BET_AMOUNT


class PayoutTests(TestCase):
    def setUp(self):
        self.team1 = mommy.make('Team')
        self.team2 = mommy.make('Team')
        self.match = mommy.make(
            'Match',
            team1=self.team1,
            team1_odds=0.80,
            team2=self.team2,
            team2_odds=0.20,
            winner=self.team1,
            valid=True
        )

    def test_payout_factor_ok(self):
        team1_payout_factor = self.match.payout_factor(self.team1)
        team2_payout_factor = self.match.payout_factor(self.team2)
        self.assertEqual(team1_payout_factor, 0.2 / 0.8)
        self.assertEqual(team2_payout_factor, 0.8 / 0.2)

    def test_winning_bet_outcome_ok(self):
        outcome = self.match.bet(self.team1)
        self.assertEqual(outcome, 0.2 / 0.8 * BET_AMOUNT)

    def test_losing_bet_outcome_ok(self):
        outcome = self.match.bet(self.team2)
        self.assertEqual(outcome, -1 * BET_AMOUNT)
