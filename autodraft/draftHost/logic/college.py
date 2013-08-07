from json import JsonObject
from draftHost import models
import nfl


class JsonCollege(JsonObject):
    functions = ['players']
    show_players = False

    def get_players(self):
        players = models.NflPlayer.objects.filter(school=self.db_object)
        players_json = []
        for p in players:
            player = nfl.JsonNflPlayer(p)
            player.show_college = False
            players_json.append(player.json_dict())
        return players_json
