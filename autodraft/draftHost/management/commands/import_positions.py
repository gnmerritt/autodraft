from django.core.management.base import NoArgsCommand
from draftHost.models import NflPosition, FantasyPosition

# path relative to manage.py
NFL_DATA_FILE = "draftHost/data/nfl_positions.txt"
FANTASY_DATA_FILE = "draftHost/data/fantasy_positions.txt"

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        importer = PositionImporter()
        importer.add_positions()
        importer.add_fantasy_positions()
        print "Positions added!"


class PositionImporter(object):
    def add_positions(self):
        try:
            data = open(NFL_DATA_FILE, 'r')
            for line in data:
                parts = line.rstrip().split(',')
                position, created = NflPosition.objects.get_or_create(**{
                    'id': parts[0],
                    'description': parts[1],
                    'abbreviation': parts[2],
                })
                if created:
                    print "added {p}".format(p=position)
                else:
                    print "got {p}".format(p=position)
            data.close()
        except IOError, e:
            print "got error {e}".format(e=e)

    def add_fantasy_positions(self):
        try:
            data = open(FANTASY_DATA_FILE, 'r')
            for line in data:
                abbrev = line.rstrip()
                position = self.find_match(abbrev)

                fantasy, created = FantasyPosition.objects.get_or_create(
                    position=position
                )
                if created:
                    print "created {f}".format(f=fantasy)
                else:
                    print "got {f}".format(f=fantasy)
            data.close()
        except IOError, e:
            print "got error {e}".format(e=e)

    def find_match(self, abbreviation):
        return NflPosition.objects.filter(abbreviation=abbreviation)[0]
