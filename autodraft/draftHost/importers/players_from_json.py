import jsonpickle

from django.db.models import Q
from draftHost import models


class GlobalData(object):
    def __init__(self):
        self.school = models.College.objects.get(pk=1)
        self.get_teams()
        self.get_positions()
        self.get_fantasy_positions()

    def get_teams(self):
        self.teams = {}
        teams = models.NflTeam.objects.all()
        for t in teams:
            self.teams[t.abbreviation] = t

    def get_positions(self):
        self.positions = {}
        positions = models.NflPosition.objects.all()
        for p in positions:
            self.positions[p.abbreviation] = p

    def get_fantasy_positions(self):
        self.fantasy_pos = {}
        positions = models.FantasyPosition.objects.all()
        for p in positions:
            self.fantasy_pos[p.position.abbreviation] = p


class PlayerMatcher(object):
    def __init__(self, json, pos):
        self.data_obj = json
        self.pos = pos
        team = self.data_obj['team']
        if not team or team == 'FA':
            self.data_obj['team'] = "UNK"

    def in_db(self):
        matches = models.NflPlayer.objects.filter(
            Q(first_name__contains=self.data_obj['first_name']) &
            Q(last_name__contains=self.data_obj['last_name']) &
            Q(position__abbreviation__contains=self.pos)
        )
        if matches:
            return True
        else:
            print "Missing player {} ".format(self.name())
            return False

    def add_to_db(self, globals):
        db_model = {
            'first_name': self.data_obj['first_name'],
            'last_name': self.data_obj['last_name'],
            'draft_year': 1,
            # These are all foreign keys, need to retrieve from globals
            'team': globals.teams[self.data_obj['team']],
            'school': globals.school,  # always wrong :-)
            'position': globals.positions[self.pos],
            'fantasy_position': globals.fantasy_pos[self.pos]
        }
        player, added = models.NflPlayer.objects.get_or_create(**db_model)
        if added:
            print "    Adding {} to DB...".format(player)

    def name(self):
        return "{} {}".format(self.data_obj['first_name'],
                              self.data_obj['last_name'])


class JsonUpdater(object):
    def __init__(self, logger, filename):
        self.logger = logger
        self.globals = GlobalData()
        pos_map = self.load_pos_map(filename)
        self.players = self.players_list(pos_map)

    def players_list(self, pos_map):
        players = []
        for pos, players_json in pos_map.iteritems():
            for player in players_json:
                pm = PlayerMatcher(player, pos)
                players.append(pm)
        return players

    def load_pos_map(self, filename):
        try:
            f = open(filename)
            json_str = self.clean_input(f.read())
            pos_map = jsonpickle.decode(json_str)
            f.close()
            return pos_map
        except:
            pass

    def clean_input(self, str):
        start_brace = str.index("{")
        end_brace = str.rfind("}") + 1
        return str[start_brace:end_brace]

    def run(self):
        for p in self.players:
            if not p.in_db():
                p.add_to_db(self.globals)
