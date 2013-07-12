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
