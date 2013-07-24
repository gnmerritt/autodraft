from django.core.management.base import NoArgsCommand
import simplejson as json

from draftHost import models

# path relative to manage.py
DATA_FILE = "draftHost/data/teams.json"

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        conferences = ConferenceImporter()
        conferences.build()

        teams = TeamImporter(self.load_json())
        teams.build()

        print "Conferences, Divisions & Teams added!"

    def load_json(self):
        try:
            json_file = open(DATA_FILE, 'r')
            data = json.load(json_file)
            return data
        except IOError, e:
            print "got error {e}".format(e=e)
            return None

class ConferenceImporter(object):
    """Adds the conferences to the DB"""
    CONFERENCES = [
        {"name":"National Football Conference", "abbreviation":"NFC",},
        {"name":"American Football Conference", "abbreviation":"AFC",},
    ]

    def build(self):
        for c in self.CONFERENCES:
            nfl_conference, created = models.NflConference.objects.get_or_create(**c)


class TeamImporter(object):
    def __init__(self, json):
        self.json = json

    def build(self):
        for conference_abbr, data in self.json.iteritems():
            conference = models.NflConference.objects.get(abbreviation=conference_abbr)

            for division_name, teams in data.iteritems():
                division, created_division = models.NflDivision.objects.get_or_create(
                    conference=conference,
                    name="{c} {d}".format(c=conference_abbr, d=division_name))

                for team in teams:
                    self.add_team(division, team)

    def add_team(self, division, team_data):
        team_data['division'] = division
        team_data['abbreviation'] = 'TODO'
        team, created = models.NflTeam.objects.get_or_create(**team_data)
        self.add_defense(team)
        if created:
            print "adding {t} to {d}".format(t=team_data, d=division.name)
        else:
            print "got {t}".format(t=team_data)

    def add_defense(self, team):
        defense = models.NflPosition.objects.filter(abbreviation="DST")[0]
        if defense:
            defense_player = {
                'position': defense,
                'first_name': 'Defense/Special Teams',
                'last_name': unicode(team),
                'team':team,
            }
            _, created = models.NflPlayer.objects.get_or_create(**defense_player)
            if created:
                print "added defense for {t}".format(t=unicode(team))
        else:
            print "need to import positions in order to add defenses"
