from django.core.management.base import BaseCommand

from draftHost.importers import players_from_json

class Command(BaseCommand):
    args = "<json file1> <json file2> etc"
    help = "Adds players from the JSON input who are missing"

    def handle(self, *args, **options):
        for json_file in args:
            print "Loading from file {} ...".format(json_file)
            updater = players_from_json.JsonUpdater(self.stdout, json_file)
            updater.run()
