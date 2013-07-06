from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
import simplejson as json

# First create the conferences
CONFERENCES = [{"name":"National Football Conference", "abbreviation":"NFC",},
               {"name":"American Football Conference", "abbreviation":"AFC",},]

# Then the divisions

# Then the teams

DATA_FILE = "../../teams.json"

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        conferences = ConferenceImporter()
        conferences.build()

        divisions = DivisionImporter(DATA_FILE)
        divisions.build()

        teams = TeamImporter(DATA_FILE)
        teams.build()

class ConferenceImporter(object):
    def build(self):
        pass

class DivisionImporter(object):
    def build(self):
        pass

class TeamImporter(object):
    def build(self):
        pass
