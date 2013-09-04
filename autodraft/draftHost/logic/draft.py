from __future__ import division
import math
import random
import datetime

from django.utils import timezone

from draftHost import models
import json
import fantasy


class PickBuilder(json.JsonObject):
    """Accumulates a list of picks associated with a draft
    Constructor argument should be a FantasyDraft model object"""
    functions = ['picks', 'selections',]

    # These will be for the draft db object, so suppress them
    show_name = False
    show_id = False

    def get_picks(self, is_team=False, options={}):
        json_picks = []
        if is_team:
            picks = models.FantasyPick.objects.filter(
                fantasy_team=self.db_object)
        else:
            picks = models.FantasyPick.objects.filter(
                fantasy_team__draft=self.db_object)
        for pick in picks:
            json = fantasy.JsonFantasyPick(pick)
            json.show_team = not is_team
            json_picks.append(json.json_dict())
        return json_picks

    def get_selections(self, is_team=False, options={}):
        selection_ids = []
        for selection in self.raw_selections(is_team):
            selection_ids.append(selection.id)
        return selection_ids

    def raw_selections(self, is_team):
        if is_team:
            return models.FantasySelection.objects.filter(
                draft_pick__fantasy_team__draft=self.db_object.draft)
        else:
            return models.FantasySelection.objects.filter(
                draft_pick__fantasy_team__draft=self.db_object)

    def add_options(self, options, json_object):
        for k, v in options.iteritems():
            json_object[k] = v


class PickAssigner(object):
    """Assigns picks for a draft"""
    def __init__(self, db_draft):
        self.db_draft = db_draft

    def build_teams_from_db(self):
        teams = models.FantasyTeam.objects.filter(draft=self.db_draft)
        teams_list = [t for t in teams.iterator()]
        random.shuffle(teams_list)
        self.teams = teams_list

    def assign_picks(self):
        """Assigns picks and returns a list of the dict objects"""
        total_picks = len(self.teams) * self.db_draft.roster.slots
        picks = []

        for i in range(1, total_picks + 1):
            pick_start, pick_expires = self.get_times_for_pick(i)
            team = self.get_team_for_pick(i)
            pick_dict = {
                "starts": pick_start,
                "expires": pick_expires,
                "pick_number": i,
                "fantasy_team": team,
            }
            picks.append(pick_dict)

        return picks

    def get_times_for_pick(self, pick_number):
        """Gets the start/expiration time for a pick"""
        start_time = self.db_draft.draft_start
        time_increment_s = self.db_draft.time_per_pick
        increase = (time_increment_s * (pick_number - 1))
        start = start_time + datetime.timedelta(seconds=increase)
        expires = start + datetime.timedelta(seconds=time_increment_s)
        return start, expires

    def get_team_for_pick(self, pick_number):
        num_teams = len(self.teams)
        current_round = math.ceil(pick_number / num_teams)
        round_pick = pick_number % num_teams
        if round_pick == 0:
            round_pick = num_teams

        # Depending on odd/even round, get the next team from the beginning
        # or end of the list of teams
        if current_round % 2 == 1:
            index = round_pick - 1
        else:
            index = num_teams - round_pick

        return self.teams[index]

    def create_picks(self, pick_list):
        """Creates the DB pick objects given a list of dicts"""
        for pick_dict in pick_list:
            pick, created = models.FantasyPick.objects.get_or_create(**pick_dict)
            if created:
                print "created pick! {p}".format(p=pick)
            else:
                print "got pick {p}".format(p=pick)

    def remove_picks(self):
        for t in self.teams:
            t.remove_picks()

    def pick_status(self):
        status = 'NONE'
        has_picks = 0
        for t in self.teams:
            if t.picks():
                has_picks += 1

        if has_picks == 0:
            return 'NONE'
        elif has_picks == len(self.teams):
            return 'ALL'
        else:
            return 'SOME'


class PickValidator(object):
    statuses = {
        'taken': [410, "That player has already been picked"],
        'pick_used': [409, "A player has already been selected with this pick"],
        'inactive': [409, "No picks active right now"],
        'success': [200, "Player drafted successfully!"],
    }

    """For a given team & draft, draft a player if available"""
    def __init__(self, auth_context):
        self.context = auth_context
        self.selection = None
        self.pick = None

        now  = timezone.now()
        picks = models.FantasyPick.objects.filter(
            fantasy_team=self.context.team,
            starts__lte=now, expires__gte=now
        )
        if picks:
            self.pick = picks[0]

    def draft_player(self, player):
        if not self.pick:
            self.status = self.statuses['inactive']
            return

        if self.pick_used():
            self.status = self.statuses['pick_used']
            return

        if self.player_taken(player):
            self.status = self.statuses['taken']
            return

        data = { 'draft_pick': self.pick,
                 'player': player, }
        self.selection = models.FantasySelection.objects.create(**data)
        self.status = self.statuses['success']
        self.success = True

    def pick_used(self):
        selections = models.FantasySelection.objects.filter(
            draft_pick=self.pick
        )
        if selections:
            self.selection = selections[0]
            return True

    def player_taken(self, player):
        selections = models.FantasySelection.objects.filter(
            player=player,
            draft_pick__fantasy_team__draft=self.context.draft,
        )
        return selections

    def get_response(self, request):
        self.code = self.status[0]
        self.message = self.status[1]
        return JsonPickResponse(self).json_response(request)


class JsonPickResponse(json.JsonObject):
    fields = [ 'success', 'message', 'code', ]
    functions = [ 'selection', ]

    def get_selection(self):
        selection = fantasy.JsonFantasySelection(self.db_object.selection)
        return selection.json_dict()
