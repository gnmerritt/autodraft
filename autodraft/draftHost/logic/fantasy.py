import datetime as d
import uuid

from draftHost import models
from json import JsonObject, JsonTime, EmailMasker
from performance import ReadOnlyCachedAttribute
import nfl, draft


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

    @ReadOnlyCachedAttribute
    def teams(self):
        return models.FantasyTeam.objects.filter(draft=self.db_object)

    def get_time_per_pick_s(self):
        return self.db_object.time_per_pick

    def get_teams(self):
        json = []
        for team in self.teams:
            json_player = JsonFantasyTeam(team)
            json_player.show_draft_id = False # already showing the draft...
            json.append(json_player.json_dict())
        return json

    def get_draft_start(self):
        return JsonTime(self.db_object.draft_start).json_dict()

    def get_roster(self):
        return JsonFantasyRoster(self.db_object.roster).json_dict()

    def get_current_time(self):
        return JsonTime(d.datetime.now()).json_dict()


class JsonFantasyTeam(JsonObject):
    fields = ['name',]
    functions = ['picks', 'selection_ids', 'draft_id', 'email', 'players']
    pick_options = { 'show_team': False, }

    show_players = False
    mask_email = True

    @ReadOnlyCachedAttribute
    def builder(self):
        return draft.PickBuilder(self.db_object)

    def get_email(self):
        email = self.db_object.email
        if self.mask_email:
            return EmailMasker(email).masked
        return email

    def get_picks(self):
        return self.builder.get_picks(is_team=True,
                                      options=self.pick_options)

    def get_selection_ids(self):
        return self.builder.get_selections(is_team=True)

    def get_draft_id(self):
        return self.db_object.draft.id

    def get_players(self):
        selections = self.builder.raw_selections(is_team=True)
        players = [s.player for s in selections]
        json_players = []
        for p in players:
            json_player = nfl.JsonNflPlayer(p)
            json_player.show_team = False
            json_players.append(json_player.json_dict())
        return json_players


class FantasyTeamCreator(object):
    """Adds a FantasyTeam to a draft given a team name & email"""
    def __init__(self, team_form_data):
        self.data = team_form_data

    def create_team(self):
        """Creates and returns the new team or None on error"""
        draft = models.FantasyDraft.objects.get(pk=self.data['draft_id'])
        if draft:
            del self.data['draft_id']
            self.data['draft'] = draft
            self.data['auth_key'] = self.get_auth_key()
            team, created = models.FantasyTeam.objects.get_or_create(**self.data)
            return team
        else:
            return None

    def get_auth_key(self):
        key = uuid.uuid4()
        return str(key)


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

    show_team = False

    def get_team(self):
        return JsonFantasyTeam(self.db_object.draft_pick.fantasy_team).json_dict()

    def get_draft_pick(self):
        pick = JsonFantasyPick(self.db_object.draft_pick)
        return pick.json_dict()

    def get_player(self):
        return nfl.JsonNflPlayer(self.db_object.player).json_dict()

    def get_when(self):
        return JsonTime(self.db_object.when).json_dict()
