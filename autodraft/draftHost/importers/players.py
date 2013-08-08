from draftHost import models

PLAYER_DATA = "/tmp/player_data.txt"

class PlayerImporter(object):
    def add_players(self):
        self.fetch_support_data()
        try:
            data = open(PLAYER_DATA, 'r')
            for line in data:
                parts = line.rstrip().split(',')
                self.add_player(parts)
            data.close()
        except IOError, e:
            print "got error {e}".format(e=e)

    def add_player(self, parts):
        print parts

    def fetch_support_data(self):
        self.colleges = models.College.objects.all()
        self.positions = models.NflPosition.objects.all()
        division = models.NflDivision.objects.filter(name="AFC South")[0]
        self.team, _ = models.NflTeams.objects.get_or_create(**{
            'name': 'Unknown',
            'city': 'Unknown',
            'abbreviation': 'Unknown',
            'division' : division,
        })
        self.dst = models.FantasyPosition.objects.filter(abbreviation="DST")[0]

    def id(id):
        """Ids in the database are 1-indexed, need to subscript into an array"""
        return id - 1

    def get_fantasy_for_position(self, position):
        fantasy = models.FantasyPosition.objects.filter(position=position)
        if fantasy:
            return fantasy[0]
        return self.dst
