from draftHost import models
from json import JsonObject
import nfl


class AuthContext(object):
    """Fetches the current team & draft from the request"""
    def __init__(self, request):
        self.request = request
        self.find_key_from_req()
        self.find_team_from_key()
        self.find_draft_from_team()

    def find_key_from_req(self):
        self.key = self.request.GET.get('key')
        if not self.key:
            self.key = self.request.POST.get('key')

    def find_team_from_key(self):
        if self.key:
            teams = models.FantasyTeam.objects.filter(auth_key=self.key)
            if teams:
                self.team = teams[0]
                return
        self.team = None

    def find_draft_from_team(self):
        if self.team:
            self.draft = self.team.draft
        else:
            self.draft = None

    def is_valid(self):
        return self.team is not None and self.draft is not None

class JsonFantasyRoster(JsonObject):
    pass ## TODO


class JsonFantasyDraft(JsonObject):
    fields = ['admin', 'team_limit',]
    functions = ['time_per_pick_s', 'draft_start', 'teams', 'roster',]

    def get_time_per_pick_s(self):
        return self.db_object.time_per_pick

    def get_team_db_objects(self):
        return models.FantasyTeam.objects.filter(draft=self.db_object)

    def get_teams(self):
        teams = self.get_team_db_objects()
        json = []
        for team in teams:
            j = JsonFantasyTeam(team)
            j.show_draft = False # already showing the draft...
            json.append(j.json_dict())
        if json:
            return json
        return None

    def get_draft_start(self):
        pass

    def get_roster(self):
        pass


class JsonFantasyTeam(JsonObject):
    fields = ['name', 'email']
    functions = ['picks', 'draft']

    def get_picks(self):
        return None

    def get_draft(self):
        return None


class JsonFantasyPick(JsonObject):
    fields = ['pick_number',]
    functions = ['team', 'expires', 'starts',]

    def get_starts(self):
        pass

    def get_expires(self):
        pass

    def get_team(self):
        return JsonFantasyTeam(self.db_object.fantasy_team).json_dict()


class PickBuilder(JsonObject):
    """Accumulates a list of picks associated with a draft
    Constructor argument should be a FantasyDraft model object"""
    functions = ['picks', 'selections',]

    # These will be for the draft db object, so suppress them
    show_name = False
    show_id = False

    def get_picks(self):
        pick_json = []
        picks = models.FantasyPick.objects.filter(fantasy_team__draft=self.db_object)
        for pick in picks:
            json_pick = JsonFantasyPick(pick)
            pick_json.append(json_pick.json_dict())
        return pick_json

    def get_selections(self):
        selections_json = []
        selections = models.FantasySelection.objects.filter(
            draft_pick__fantasy_team__draft=self.db_object)
        for selection in selections:
            json_selection = JsonFantasySelection(selection)
            selections_json.append(json_selection.json_dict())
        return selections_json

class JsonFantasySelection(JsonObject):
    functions = ['team', 'draft_pick', 'player', 'when',]

    def get_team(self):
        return JsonFantasyTeam(self.db_object.draft_pick.fantasy_team).json_dict()

    def get_draft_pick(self):
        pick = JsonFantasyPick(self.db_object.draft_pick)
        return pick.json_dict()

    def get_player(self):
        return nfl.JsonNflPlayer(self.db_object.player).json_dict()

    def get_when(self):
        pass
