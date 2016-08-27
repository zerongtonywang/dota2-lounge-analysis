from django.core.exceptions import ValidationError
from app.models import Team, Match
from bs4 import BeautifulSoup as bs
import requests
import json
import re


def load_matches():
    with open('app/matches.json') as data_file:
        matches_data = json.load(data_file)

    print('Preparing and validating match data sets...', end='', flush=True)
    prep_datas = []
    for match_data in matches_data:
        prep_data = {
            'id': match_data['match'],
            'datetime': match_data['when'],
            'finished': True if match_data['closed'] == '1' else False,
            'event': match_data['event'],
            'bestof': match_data['format'],
        }
        prep_data['team1'], _ = Team.objects.get_or_create(
            name=match_data['a']
        )

        prep_data['team2'], _ = Team.objects.get_or_create(
            name=match_data['b']
        )

        if match_data['winner'] == 'a':
            prep_data['winner'] = prep_data['team1']
        elif match_data['winner'] == 'b':
            prep_data['winner'] = prep_data['team2']

        match = Match(**prep_data)
        match.full_clean()
        prep_datas.append(prep_data)

    print('Ok')
    print('{} matches prepared'.format(len(prep_datas)))
    print('Creating matches...', end='', flush=True)
    for prep_data in prep_datas:
        Match.objects.create(**prep_data)
    print('Ok')


def scrape_odds():
    print('Starting scrape...')
    url = 'http://dota2lounge.com/match?m={}'
    progress = 0
    for i in range(Match.objects.all().count() + 1):
        site = requests.get(url.format(i))
        soup = bs(site.text, 'lxml')
        if 'Match' in soup.title.text:
            r = re.compile('[\s\S]+Match ([0-9]+)')
            match_id = int(r.match(soup.title.text).group(1))
            if match_id > progress:
                progress = match_id
                print('Scraping match {}...'.format(match_id), end='', flush=True)
            else:
                print('Already scraped match {}'.format(match_id))
                continue
        else:
            print('Could not scrape match {}'.format(i))
            continue

        match = Match.objects.get(id=match_id)
        team_divs = soup.find_all('div', class_='team')
        for team_div in team_divs:
            team_div = team_div.parent
            team_name = team_div.b.text
            team_odds = int(team_div.i.text.strip('%')) / 100
            r = re.compile('[\s\S]+, \'([ab])\'')
            team_annotation = r.match(team_div.parent['onclick']).group(1)

            if team_annotation == 'a':
                match.team1_odds = team_odds
                if '(win)' in team_name:
                    match.winner = match.team1
            elif team_annotation == 'b':
                match.team2_odds = team_odds
                if '(win)' in team_name:
                    match.winner = match.team1
        match.save()
        print('OK')


def update_winners():
    with open('app/matches.json') as data_file:
        matches_data = json.load(data_file)

    for match_data in matches_data:
        try:
            match = Match.objects.get(id=int(match_data['match']))
        except Match.DoesNotExist:
            raise ValidationError('Match {} does not exist.'.format(match_data['match']))

        if match_data['winner'] == 'a':
            match.winner = match.team1
        elif match_data['winner'] == 'b':
            match.winner = match.team2

        match.save()
        print('Match {} update winner complete.'.format(match.id))


def refresh_matches():
    print('Refreshing matches...', end='', flush=True)
    for match in Match.objects.all():
        match.save()
    print('Ok')
