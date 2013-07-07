from django.core.management.base import NoArgsCommand
from draftHost.models import Position

# path relative to manage.py
DATA_FILE = "draftHost/data/positions.txt"

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        importer = PositionImporter()
        importer.build()

        print "Positions added!"

class PositionImporter(object):
    def build(self):
        try:
            data = open(DATA_FILE, 'r')
            for line in data:
                parts = line.rstrip().split(',')
                print parts
                position, created = Position.objects.get_or_create(
                    abbreviation = parts[0],
                    desc = parts[1]
                    )
                if created:
                    print "added {p}".format(p=position)
                else:
                    print "got {p}".format(p=position)
        except IOError, e:
            print "got error {e}".format(e=e)
