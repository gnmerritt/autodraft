from json import JsonObject

class JsonNflPlayer(JsonObject):
    fields = ['first_name', 'last_name', 'jersey_number']

    def __init__(self, db_nfl_player):
        super(JsonNflPlayer, self).__init__(db_nfl_player)
        self.functions = {
            'team': self.get_team,
            'position': self.get_position,
        }

    def get_team(self):
        return JsonNflTeam(self.db_object.team).json_dict()

    def get_position(self):
        return self.db_object.position.abbreviation

class JsonNflTeam(JsonObject):
    fields = ['city']

    def __init__(self, db_nfl_team):
        super(JsonNflTeam, self).__init__(db_nfl_team)
        self.functions = {
            'divison' : self.get_division,
        }

    def get_division(self):
        return JsonNflDivision(self.db_object.divison).json_dict()


class JsonNflDivision(JsonObject):
    def __init__(self, db_nfl_div):
        super(JsonNflDivision, self).__init__(db_nfl_div)
        self.functions = {
            'conference' : self.get_conference,
        }

    def get_conference(self):
        return JsonNflConference(self.db_object.conference).json_dict()

class JsonNflConference(JsonObject):
    pass # No extra fields needed
