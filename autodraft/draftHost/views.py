from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import django.http.response
from django.core.exceptions import PermissionDenied

from brake.decorators import ratelimit

from draftHost import models
from draftHost.logic import nfl, fantasy, auth, draft, json, college
from draftHost.logic import search as s
from draftHost.logic.auth import AuthContext as AuthContext

def get_context_or_error(request):
    """Tries to build a AuthContext, raises an error on failure"""
    context = AuthContext(request)
    if context.is_valid():
        return context
    raise django.core.exceptions.PermissionDenied("invalid auth key")

@ratelimit(rate="30/m")
def draft_key(request):
    context = get_context_or_error(request)
    return fantasy.JsonFantasyDraft(context.draft).json_response(request)

@ratelimit(rate="30/m")
def draft_id(request, id):
    draft = get_object_or_404(models.FantasyDraft, pk=id)
    return fantasy.JsonFantasyDraft(draft).json_response(request)

def picks(request):
    context = get_context_or_error(request)
    picks = draft.PickBuilder(context.draft)
    picks.now = timezone.now()
    return picks.json_response(request)

@ratelimit(rate="10/m")
def make_pick(request, player_id):
    if request.method == "POST" or request.method == "GET":
        context = get_context_or_error(request)
        player = get_object_or_404(models.NflPlayer, pk=player_id)
        validator = draft.PickValidator(context)
        validator.draft_player(player)
        return validator.get_response(request)
    elif request.method == "OPTIONS":
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = "X-Requested-With"
        response['Access-Control-Max-Age'] = "1800"
    else:
        raise django.http.response.BadHeaderError("only POST/OPTIONS allowed")

def player(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    json_player = nfl.JsonNflPlayer(db_player)
    return json_player.json_response(request)

def player_status(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    context = get_context_or_error(request)
    json_player = nfl.JsonNflPlayer(db_player)
    json_player.draft = context.draft
    json_player.show_fantasy_team = True
    return json_player.json_response(request)

@ratelimit("60/m", block=True)
def search(request, name=None, position=None):
    return s.SearchRunner() \
      .name(name) \
      .position(position) \
      .json_results() \
      .json_response(request)

def team_id(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    return team_response(team, request)

def team_info_name(request, name):
    team = get_object_or_404(models.FantasyTeam, name=name)
    return team_response(team, request)

def current_team(request):
    context = get_context_or_error(request)
    return team_response(context.team, request)

def team_response(db_team, request):
    json_team = fantasy.JsonFantasyTeam(db_team)
    json_team.show_players = True
    return json_team.json_response(request)

def fantasy_team_players(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    json_team = fantasy.JsonFantasyTeam(team)
    json_team.show_players = True
    return json_team.json_response(request)

def nfl_teams(request):
    teams = models.NflTeam.objects.all().exclude(name="Unknown")
    teams_json = [nfl.JsonNflTeam(t).json_dict() for t in teams]
    return json.obj_to_json({'teams': teams_json}, request)

def nfl_team(request, id):
    return nfl_team_with_players(request, id, include_players=False)

@ratelimit(block=True)
def nfl_team_with_players(request, id, include_players=True):
    team = get_object_or_404(models.NflTeam, pk=id)
    json_team = nfl.JsonNflTeam(team)
    if include_players:
        json_team.show_players = True
    return json_team.json_response(request)

def nfl_divisions(request):
    divisions = models.NflDivision.objects.all()
    divisons_json = [nfl.JsonNflDivision(d).json_dict()
                     for d in divisions]
    return json.obj_to_json({'divisions':divisons_json}, request)

def nfl_conferences(request):
    conferences = models.NflConference.objects.all()
    conferences_json = [nfl.JsonNflConference(c).json_dict()
                        for c in conferences]
    return json.obj_to_json({'conferences':conferences_json}, request)

def nfl_positions(request):
    positions = models.NflPosition.objects.all()
    positions_json = [nfl.JsonNflPosition(p).json_dict()
                      for p in positions]
    return json.obj_to_json({'positions':positions_json}, request)

def colleges(request):
    colleges = models.College.objects.all().exclude(name="Unknown")
    colleges_json = []
    for c in colleges:
        colleges_json.append(college.JsonCollege(c).json_dict())
    return json.obj_to_json({'colleges':colleges_json}, request)

@ratelimit(block=True)
def college_players(request, id):
    c = get_object_or_404(models.College, pk=id)
    college_json = college.JsonCollege(c)
    college_json.show_players = True
    return college_json.json_response(request)

def my_team(request, key):
    team = get_object_or_404(models.FantasyTeam, auth_key=key)
    draft = fantasy.JsonFantasyDraft(team.draft)
    context = {
        'team': team,
        'draft': draft.json_dict(),
    }
    return render(request, 'draftHost/team_page.html', context)

@ratelimit(rate="60/m", block=True)
def index(request):
    now = timezone.now()
    drafts = []
    for d in models.FantasyDraft.objects.all():
        json = fantasy.JsonFantasyDraft(d).json_dict()
        if d.draft_start > now:
            json['active'] = True

            if len(json['teams']) < d.team_limit:
                json['registration'] = auth.TeamRegisterForm()
        drafts.append(json)
    drafts.sort(key=lambda d: d['draft_start']['utc'], reverse=True)
    context = {
        'drafts': drafts,
    }
    return render(request, 'draftHost/index.html', context)

def register(request):
    if request.method == 'POST':
        form = auth.TeamRegisterForm(request.POST)
        if form.is_valid():
            creator = fantasy.FantasyTeamCreator(form.cleaned_data)
            team = creator.create_team()
            if team:
                args = {
                    'key': team.auth_key,
                }
                private_team_page = reverse('draftHost:my_team', kwargs=args)
                return HttpResponseRedirect(private_team_page)
            else:
                return HttpResponseRedirect(reverse('draftHost:index'))

        return index(request)
    else:
        raise django.http.response.BadHeaderError("only POST allowed")

@ratelimit(rate="60/m", block=True)
def draft_detail(request, id, ajax_only=False):
    draft = get_object_or_404(models.FantasyDraft, pk=id)
    json_draft = fantasy.JsonFantasyDraft(draft).json_dict()
    now = timezone.now()
    is_active = draft.is_active(now)

    selections_queryset = models.FantasySelection.objects.filter(
        draft_pick__fantasy_team__draft=draft
    )
    selections = []
    for s in selections_queryset:
        selection_json = fantasy.JsonFantasySelection(s)
        selection_json.show_team = True
        selections.append(selection_json.json_dict())
    selections.sort(key=lambda s: s['draft_pick']['pick_number'],
                    reverse=is_active)

    picks_queryset = models.FantasyPick.objects.filter(
        fantasy_team__draft=draft
    )
    picks = []
    for p in picks_queryset:
        if now > p.expires:
            continue
        json = fantasy.JsonFantasyPick(p)
        json.now = now
        picks.append(json.json_dict())
    picks.sort(key=lambda p: p['pick_number'])
    shown_picks = len(json_draft['teams']) + 5

    context = {
        'draft': json_draft,
        'picks': picks[:shown_picks],
        'selections': selections,
        'is_active': is_active,
        'poll_time': 10000, # 10 seconds
    }
    if ajax_only:
        return render(request, 'draftHost/detail_ajax.html', context)
    else:
        return render(request, 'draftHost/draft.html', context)

@ratelimit(rate="60/m", block=True)
def draft_pick_ajax(request, id):
    return draft_detail(request, id, ajax_only=True)

def documentation(request):
    return render(request, 'draftHost/documentation.html', {})
