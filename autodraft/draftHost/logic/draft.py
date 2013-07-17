from __future__ import division
import math
import random

from draftHost import models
from json import JsonObject
import fantasy


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
            json_pick = fantasy.JsonFantasyPick(pick)
            pick_json.append(json_pick.json_dict())
        return pick_json

    def get_selections(self):
        selections_json = []
        selections = models.FantasySelection.objects.filter(
            draft_pick__fantasy_team__draft=self.db_object)
        for selection in selections:
            json_selection = fantasy.JsonFantasySelection(selection)
            selections_json.append(json_selection.json_dict())
        return selections_json


class PickAssigner(object):
    """Assigns picks for a draft"""
    def __init__(self, db_draft):
        self.db_draft = db_draft

    def build_teams_from_db(self):
        teams = models.FantasyTeam.objects.filter(draft=self.db_draft)
        random.shuffle(teams)
        self.teams = teams

    def assign_picks(self):
        """Assigns picks and returns a list of the dict objects"""
        total_picks = len(self.teams) * self.db_draft.rounds
        picks = []

        for i in range(1, total_picks + 1):
            pick_start, pick_expires = self.get_times_for_pick(i)
            team = self.get_team_for_pick(i)
            pick_dict = {
                "starts": pick_start,
                "expires": pick_expires,
                "pick_number": i,
                "team": team,
            }
            picks.append(pick_dict)

        return picks

    def get_times_for_pick(self, pick_number):
        """Gets the start/expiration time for a pick"""
        start_time = self.db_draft.draft_start
        time_increment_s = self.db_draft.time_per_pick
        start = start_time + (time_increment_s * (pick_number - 1))
        expires = start + time_increment_s
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
