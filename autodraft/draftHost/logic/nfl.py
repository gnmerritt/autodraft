from json import JsonObject


class JsonNflPlayer(JsonObject):
    fields = ['first_name', 'last_name']
    functions = ['team', 'position']

    def get_team(self):
        return JsonNflTeam(self.db_object.team).json_dict()

    def get_position(self):
        return self.db_object.position.abbreviation


class JsonNflTeam(JsonObject):
    fields = ['city']
    functions = ['division']

    def get_division(self):
        return JsonNflDivision(self.db_object.divison).json_dict()


class JsonNflDivision(JsonObject):
    functions = ['conference']

    def get_conference(self):
        return JsonNflConference(self.db_object.conference).json_dict()


class JsonNflConference(JsonObject):
    pass # No extra fields needed
