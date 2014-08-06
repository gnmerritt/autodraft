from json import JsonObject
from draftHost import models
import fantasy, college


class JsonNflPosition(JsonObject):
    pass # No extra fields needed


class JsonNflPlayer(JsonObject):
    fields = ['first_name', 'last_name']
    functions = ['team', 'college',
                 'nfl_position', 'fantasy_position',
                 'fantasy_team', 'draft_year']

    show_fantasy_team = False
    draft = None

    def get_team(self):
        if self.db_object.team.name != "Unknown":
            return JsonNflTeam(self.db_object.team).json_dict()

    def get_nfl_position(self):
        return JsonNflPosition(self.db_object.position).json_dict()

    def get_fantasy_position(self):
        return self.db_object.fantasy_position.position.abbreviation

    def get_college(self):
        return college.JsonCollege(self.db_object.school).json_dict()

    def get_fantasy_team(self):
        if not self.draft:
            return False
        selections = models.FantasySelection.objects.filter(player=self.db_object,
                         player__draft_pick__fantasy_team__draft=self.draft)
        if not selections:
            return False
        fantasy_team = selections[0].draft_pick.fantasy_team
        json_team = fantasy.JsonFantasyTeam(fantasy_team)
        # Only want the stub team info, shut off the other fields
        json_team.show_picks = False
        json_team.show_selections = False
        return json_team.json_dict()

    def get_draft_year(self):
        """Return the draft year only if it's valid"""
        if self.db_object.draft_year > 1:
            return self.db_object.draft_year
        return None


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
