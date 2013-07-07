from django.http import HttpResponse
import simplejson as json

def obj_to_json(object):
    # TODO: add data/pagination objects
    return HttpResponse(json.dumps(object), mimetype="application/json")

class JsonNflPlayer(object):
    def __init__(self, db_nfl_player):
        self.d = {}
        self.d['first_name'] = db_nfl_player.first_name
        self.d['last_name'] = db_nfl_player.last_name
        self.d['jersey_number'] = db_nfl_player.jersey_number
        self.d['team'] = unicode(db_nfl_player.team)
        self.d['position'] = db_nfl_player.position.abbreviation

    def json_response(self):
        return obj_to_json(self.d)
