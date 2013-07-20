from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import django.http.response

import draftHost.models as models
import draftHost.logic.nfl as nfl
import draftHost.logic.fantasy as fantasy
import draftHost.logic.draft as drafter
from draftHost.logic.auth import AuthContext as AuthContext

def get_context_or_error(request):
    """Tries to build a AuthContext, raises an error on failure"""
    context = AuthContext(request)
    if context.is_valid():
        return context
     ## TODO - this should probably be a different error
    raise django.http.response.BadHeaderError("invalid auth key")

def draft(request):
    context = get_context_or_error(request)
    return fantasy.JsonFantasyDraft(context.draft).json_response()

def draft_id(request, id):
    draft = get_object_or_404(models.FantasyDraft, pk=id)
    return fantasy.JsonFantasyDraft(draft).json_response()

def picks(request):
    context = get_context_or_error(request)
    picks = drafter.PickBuilder(context.draft)
    return picks.json_response()

def make_pick(request, pick_id, player_id):
    ## TODO
    context = get_context_or_error(request)
    return HttpResponse("picks/make/{p}/player/{who}/"
                        .format(p=pick_id, who=player_id))

def player(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    json_player = nfl.JsonNflPlayer(db_player)
    return json_player.json_response()

def search(request, query):
    ## TODO
    return HttpResponse("search/{q}".format(q=query))

def team_id(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    return team_response(team)

def team_info_name(request, name):
    team = get_object_or_404(models.FantasyTeam, name=name)
    return team_response(team)

def current_team(request):
    context = get_context_or_error(request)
    return team_response(context.team)

def team_response(db_team):
    json_team = fantasy.JsonFantasyTeam(db_team)
    return json_team.json_response()

def register(request):
    drafts = [fantasy.JsonFantasyDraft(k).json_dict()
              for k in models.FantasyDraft.objects.all()]
    context = {
        'drafts': drafts,
    }
    return render(request, 'draftHost/registration.html', context)
