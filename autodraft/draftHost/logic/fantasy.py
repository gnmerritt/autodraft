from json import JsonObject
import nfl


class JsonFantasyTeam(JsonObject):
    fields = ['name', 'email']
    functions = ['picks', 'draft']

    def get_picks(self):
        return None

    def get_draft(self):
        return None


class JsonFantasyPick(JsonObject):
    fields = ['expires', 'pick_number',]
    functions = ['team',]

    def get_team(self):
        return JsonFantasyTeam(self.db_object.fantasy_team).json_dict()


class JsonFantasySelection(JsonObject):
    fields = ['when',]
    functions = ['team', 'draft_pick', 'player']

    def get_team(self):
        return JsonFantasyTeam(self.db_object.fantasy_team).json_dict()

    def get_draft_pick(self):
        pick = JsonFantasyPick(self.db_object.draft_pick)
        pick.show_team = False
        return pick.json_dict()

    def get_player(self):
        return nfl.JsonNflPlayer(self.db_object.player).json_dict()
