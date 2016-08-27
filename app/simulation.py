from datetime import timedelta

from app.models import Match
from d2lbetting.settings import TRAIN_PERIOD, BET_AMOUNT, HOUSE_RESERVE


class Simulation:
    def __init__(self):
        self.end_datetime = Match.objects.latest().datetime
        self.start_datetime = self.end_datetime - timedelta(days=365)
        # self.start_datetime = self.start_datetime_after_training()
        self.starting_amount = 0
        self.current_amount = self.starting_amount
        self.bets_won = 0
        self.queryset = self.get_queryset()

    def print_setup(self):
        print('Begin betting simulation...')
        print('Match count: {}'.format(self.queryset.count()))
        print('Start datetime: {}'.format(self.start_datetime))
        print('End datetime: {}'.format(self.end_datetime))
        print('Model training period: {} days'.format(TRAIN_PERIOD))
        print('Bet amount per match: ${}'.format(BET_AMOUNT))
        print('House reserve set at: {}'.format(HOUSE_RESERVE))
        print('Starting amount at: ${}'.format(self.starting_amount))

    def print_final(self):
        print('Final amount at: ${}'.format(self.current_amount))
        print('Accuracy: {}'.format(
            1.0 * self.bets_won / self.queryset.count()
        ))

    def simulate(self):
        self.current_amount = self.starting_amount
        for match in self.queryset:
            outcome = match.auto_bet()
            self.current_amount += outcome
            if outcome > 0:
                self.bets_won += 1
            print(self.current_amount)
        self.print_setup()
        self.print_final()

    def get_queryset(self):
        queryset = Match.objects.time_period(
            self.start_datetime,
            self.end_datetime
        ).valid()
        return queryset

    def start_datetime_after_training(self):
        old_start = Match.objects.get(id=1).datetime
        new_start = old_start + timedelta(days=TRAIN_PERIOD)
        return new_start

    def start_datetime_past(self, days):
        start_datetime = self.end_datetime - timedelta(days=days)
        return start_datetime
