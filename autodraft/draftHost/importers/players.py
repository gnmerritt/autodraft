from draftHost import models

PLAYER_DATA = "/tmp/player_data.txt"

class PlayerImporter(object):
    DATA_FORMAT = ['id', 'first_name', 'last_name',
                   'position_id', 'school_id', 'draft_year']

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
        data = dict(zip(self.DATA_FORMAT, parts))
        data['school'] = self.colleges[self.id(data['school_id'])]
        del data['school_id']
        position = self.positions[self.id(data['position_id'])]
        data['position'] = position
        del data['position_id']
        data['fantasy_position'] = self.get_fantasy_for_position(position)
        data['team'] = self.team
        del data['id']

        player, added = models.NflPlayer.objects.get_or_create(**data)
        if added:
            print "added player {p}".format(p=player)

    def fetch_support_data(self):
        self.colleges = models.College.objects.all()
        self.positions = models.NflPosition.objects.all()
        division = models.NflDivision.objects.filter(name="AFC South")[0]
        self.team, _ = models.NflTeam.objects.get_or_create(**{
            'name': 'Unknown',
            'city': 'Unknown',
            'abbreviation': 'Unknown',
            'division' : division,
        })
        self.dst = models.FantasyPosition.objects.filter(position__abbreviation="DST")[0]

    def id(self, id_str):
        """Ids in the database are 1-indexed, need to subscript into an array"""
        id = int(id_str)
        if id > 0:
            return id - 1
        return 0

    def get_fantasy_for_position(self, position):
        fantasy = models.FantasyPosition.objects.filter(position=position)
        if fantasy:
            return fantasy[0]
        return self.dst
