from django.core.management.base import NoArgsCommand
import simplejson as json

from draftHost.models import NflConference, NflDivision, NflTeam

# path relative to manage.py
DATA_FILE = "draftHost/data/teams.json"

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        conferences = ConferenceImporter()
        conferences.build()

        teams = TeamImporter(self.load_json())
        teams.build()

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
            nfl_conference, created = NflConference.objects.get_or_create(**c)


class TeamImporter(object):
    def __init__(self, json):
        self.json = json

    def build(self):
        for conference_abbr, data in self.json.iteritems():
            conference = NflConference.objects.get(abbreviation=conference_abbr)

            for division_name, teams in data.iteritems():
                division, created_division = \
                  NflDivision.objects.get_or_create(name="{c} {d}"
                                                    .format(c=conference_abbr, d=division_name))

    def add_team(self, division, team_data):
        pass
