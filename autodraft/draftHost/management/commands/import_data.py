from django.core.management.base import NoArgsCommand

from draftHost.importers import positions, conferences, colleges, teams, players


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        p = positions.PositionImporter()
        p.add_positions()
        p.add_fantasy_positions()

        print "Positions added!"

        c = conferences.ConferenceImporter()
        c.build()

        print "Conferences added!"

        c2 = colleges.CollegeImporter()
        c2.build()

        print "Colleges added!"

        t = teams.TeamImporter()
        t.build()

        print "Teams added!"

        p2 = players.PlayerImporter()
        p2.add_players()

        print "Players added!"
