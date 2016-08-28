from datetime import timedelta

from app.models import Match
from d2lbetting.settings import SimulationSettings


class Simulation(SimulationSettings):
    def __init__(self, simulation_settings=None):
        if simulation_settings:
            self.set_attributes(simulation_settings)
        self.end_datetime = Match.objects.latest().datetime - timedelta(days=self.DELTA_END_DAYS)
        self.start_datetime = self.end_datetime - timedelta(days=self.PERIOD)
        self.starting_amount = 0
        self.current_amount = self.starting_amount
        self.bets_won = 0
        self.queryset = self.get_queryset()
        self.matches_count = self.queryset.count()

    def simulate(self):
        self.current_amount = self.starting_amount
        for match in self.queryset:
            outcome = match.auto_bet()
            self.current_amount += outcome
            if outcome > 0:
                self.bets_won += 1
            elif outcome == 0:
                self.matches_count -= 1
            self.console(match)

        self.print_setup()
        self.print_final()

    def print_setup(self):
        print('Simulation completed...')
        print('Match count: {}/{}'.format(self.matches_count, self.queryset.count()))
        print('Start datetime: {}'.format(self.start_datetime))
        print('End datetime: {}'.format(self.end_datetime))
        print('Model training period: {} days'.format(self.TRAIN_PERIOD))
        print('House reserve set at: {}'.format(self.HOUSE_RESERVE))
        print('Bet amount per match: ${}'.format(self.BET_AMOUNT))
        print('Starting amount at: ${}'.format(self.starting_amount))

    def print_final(self):
        profit = self.current_amount - self.starting_amount
        if self.matches_count > 0:
            average_return_per_match = profit / self.matches_count / self.BET_AMOUNT
            accuracy = 1.0 * self.bets_won / self.matches_count
        else:
            average_return_per_match = 0
            accuracy = 0
        print('Final amount at: ${}'.format(self.current_amount))
        print('Accuracy: {}'.format(accuracy))
        print('Average return per match: {}'.format(average_return_per_match))

    def console(self, match):
        if self.CONSOLE == 'FULL':
            self.console_log(match)
        elif self.CONSOLE == 'AGAINST':
            if match.winner != match.crowd_favourite():
                self.console_log(match)

    def console_log(self, match):
        print('Match {}:'.format(match.id))
        print('Team odds: {}: {} vs {}: {}'.format(
            match.team1, match.team1_odds,
            match.team2, match.team2_odds
        ))
        print('Team factors: {}: {} vs {}: {}'.format(
            str(match.team1), match.bet_factor(match.team1),
            str(match.team2), match.bet_factor(match.team2))
        )
        team = match.bet_method()
        if team:
            print('Bet on: {}'.format(match.bet_method()))
        else:
            print('Did not bet')
        print('Winner: {}'.format(match.winner))
        if team == match.winner:
            print('Payout: {}'.format(match.payout(team)))
        elif team == match.reverse_team(match.winner):
            print('Payout: -{}'.format(self.BET_AMOUNT))
        if team:
            print('Current amount: {}'.format(self.current_amount))
        print('==============================================================')

    def get_queryset(self):
        queryset = Match.objects.time_period(
            self.start_datetime,
            self.end_datetime
        ).valid()
        return queryset
