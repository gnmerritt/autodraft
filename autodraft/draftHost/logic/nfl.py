from json import JsonObject
from draftHost import models

class JsonNflPosition(JsonObject):
    pass # No extra fields needed

class JsonNflPlayer(JsonObject):
    fields = ['first_name', 'last_name']
    functions = ['team', 'position']

    def get_team(self):
        return JsonNflTeam(self.db_object.team).json_dict()

    def get_position(self):
        return JsonNflPosition(self.db_object.position).json_dict()


class JsonNflTeam(JsonObject):
    fields = ['city',]
    functions = ['division', 'players',]

    show_players = False

    def get_division(self):
        return JsonNflDivision(self.db_object.division).json_dict()

    def get_players(self):
        players = models.NflPlayer.objects.filter(team=self.db_object)
        players_json = []
        for p in players:
            json = JsonNflPlayer(p)
            json.show_team = False
            players_json.append(json.json_dict())
        return players_json


class JsonNflDivision(JsonObject):
    functions = ['conference',]

    def get_conference(self):
        return JsonNflConference(self.db_object.conference).json_dict()


class JsonNflConference(JsonObject):
    pass # No extra fields needed
