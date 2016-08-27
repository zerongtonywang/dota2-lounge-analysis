SECRET_KEY = 'c^i)1=av5m!y567=7vu-1i_pnr-58(uz+9j%zkq-9t1o306weq'
DEBUG = True
DEV = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2lbetting',
        'USER': 'd2lbettinguser',
        'PASSWORD': 'd2lbettingpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}


class Algo:
    def team1_bet_factor(self):
        winrate = self.team1.past_winrate(self.datetime)
        mean_odds = float(self.team1.past_mean_odds(self.datetime))
        payout_factor = float(self.payout_factor(self.team1))
        # ALGO, made with <3 by Dr. David
        bet_factor = payout_factor * float(self.team2_odds) * winrate / mean_odds
        return bet_factor

    def team2_bet_factor(self):
        winrate = self.team2.past_winrate(self.datetime)
        mean_odds = float(self.team2.past_mean_odds(self.datetime))
        payout_factor = float(self.payout_factor(self.team2))
        # ALGO, made with <3 by Dr. David
        bet_factor = payout_factor * float(self.team1_odds) * winrate / mean_odds
        return bet_factor
