from json import JsonObject
import nfl


class JsonFantasyTeam(JsonObject):
    fields = ['name', 'email']
    functions = ['picks', 'draft']

    show_picks = False
    show_draft = False

    def get_picks(self):
        if self.show_picks:
            pass
        return None

    def get_draft(self):
        if self.show_draft:
            pass
        return None


class JsonFantasyPick(JsonObject):
    fields = ['expires', 'pick_number',]
    functions = ['team',]

    show_team = True

    def get_team(self):
        if self.show_team:
            return JsonFantasyTeam(self.db_object.fantasy_team).json_dict()
        return None


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
