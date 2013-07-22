from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
import django.http.response

from draftHost import models
from draftHost.logic import nfl, fantasy, auth, draft
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
    picks = draft.PickBuilder(context.draft)
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

def my_team(request, key):
    team = get_object_or_404(models.FantasyTeam, auth_key=key)
    context = {
        'team': team,
    }
    return render(request, 'draftHost/team_page.html', context)

def draft_page(request):
    drafts = [fantasy.JsonFantasyDraft(k).json_dict()
              for k in models.FantasyDraft.objects.all()]
    for draft in [d for d in drafts
                  if len(d['teams']) < d['team_limit']]:
        form = auth.TeamRegisterForm()
        draft['registration'] = form
    context = {
        'drafts': drafts,
    }
    return render(request, 'draftHost/draft_page.html', context)

def register(request):
    if request.method == 'POST':
        form = auth.TeamRegisterForm(request.POST)
        if form.is_valid():
            creator = fantasy.FantasyTeamCreator(form.cleaned_data)
            team = creator.create_team()
            if team:
                args = {}
                private_team_page = reverse('draftHost:team_html', kwargs=args)
                return HttpResponseRedirect(private_team_page)
            else:
                return HttpResponseRedirect(reverse('draftHost:draft_page'))

        raise django.http.response.BadHeaderError("BAD FORM") ## TODO
    else:
        raise django.http.response.BadHeaderError("only POST allowed")
