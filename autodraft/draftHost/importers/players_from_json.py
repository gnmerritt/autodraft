import jsonpickle

from django.db.models import Q
from draftHost import models

class GlobalData(object):
    pass

class PlayerMatcher(object):
    def __init__(self, json, pos):
        self.data_obj = json
        self.pos = pos

    def add_globals(self):
        """Adds NflTeam, College, position, fantasy position"""
        pass

    def in_db(self):
        matches = models.NflPlayer.objects.filter(
            Q(first_name__contains=self.data_obj['first_name']) &
            Q(last_name__contains=self.data_obj['last_name']) &
            Q(position__abbreviation__contains=self.pos)
        )
        if matches:
            print "Found player {} ".format(self.name())
            return True
        else:
            print "Missing player {} ".format(self.name())
            return False

    def add_to_db(self, globals):
        print "    Adding {} to DB...".format(self.name())

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
        start_brace = str.index("{");
        end_brace = str.rfind("}") + 1
        return str[start_brace:end_brace]

    def run(self):
        for p in self.players:
            if not p.in_db():
                p.add_to_db(self.globals)
