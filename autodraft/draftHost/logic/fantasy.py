import datetime.datetime as time

from draftHost import models
from json import JsonObject
import nfl, draft


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


class JsonTime(JsonObject):
    """Standard time representation, input object should be a
    datetime.datetime"""
    functions = ['utc', 'str']

    def get_utc(self):
        pass

    def get_str(self):
        pass


class JsonFantasyRoster(JsonObject):
    fields = ['slots',]
    show_id = False


class JsonFantasyDraft(JsonObject):
    fields = ['admin', 'team_limit',]
    functions = ['time_per_pick_s',
                 'teams',
                 'roster',
                 'draft_start',
                 'current_time',]

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
        return JsonTime(self.db_object.draft_start).json_dict()

    def get_roster(self):
        return JsonFantasyRoster(self.db_object.roster).json_dict()

    def get_current_time(self):
        return JsonTime(time.now()).json_dict()


class JsonFantasyTeam(JsonObject):
    fields = ['name', 'email']
    functions = ['picks', 'selections', 'draft']
    pick_options = { 'show_team': False, }

    def get_picks(self):
        picks = draft.PickBuilder(self.db_object)
        return picks.get_picks(isTeam=True,
                               options=self.pick_options)

    def get_selections(self):
        picks = draft.PickBuilder(self.db_object)
        return picks.get_selections(isTeam=True)

    def get_draft(self):
        selections = PickBuilder(self.db_object)
        return selections.get_selections(isTeam=True,
                                         options=self.pick_options)


class JsonFantasyPick(JsonObject):
    fields = ['pick_number',]
    functions = ['team', 'expires', 'starts',]

    def get_starts(self):
        return JsonTime(self.db_object.starts).json_dict()

    def get_expires(self):
        return JsonTime(self.db_object.expires).json_dict()

    def get_team(self):
        return JsonFantasyTeam(self.db_object.fantasy_team).json_dict()


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
        return JsonTime(self.db_object.when).json_dict()
