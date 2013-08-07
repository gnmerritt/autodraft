from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
import django.http.response

from draftHost import models
from draftHost.logic import nfl, fantasy, auth, draft, json, college
from draftHost.logic.auth import AuthContext as AuthContext

def get_context_or_error(request):
    """Tries to build a AuthContext, raises an error on failure"""
    context = AuthContext(request)
    if context.is_valid():
        return context
     ## TODO - this should probably be a different error
    raise django.http.response.BadHeaderError("invalid auth key")

def draft_key(request):
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

def player_status(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    context = get_context_or_error(request)
    json_player = nfl.JsonNflPlayer(db_player)
    json_player.draft = context.draft
    json_player.show_fantasy_team = True
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

def fantasy_team_players(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    json_team = fantasy.JsonFantasyTeam(team)
    json_team.show_players = True
    return json_team.json_response()

def nfl_teams(request):
    teams = models.NflTeam.objects.all()
    teams_json = [nfl.JsonNflTeam(t).json_dict() for t in teams]
    return json.obj_to_json({'teams': teams_json})

def nfl_team(request, id):
    return nfl_team_with_players(request, id, include_players=False)

def nfl_team_with_players(request, id, include_players=True):
    team = get_object_or_404(models.NflTeam, pk=id)
    print "got team {t}".format(t=team)
    json_team = nfl.JsonNflTeam(team)
    if include_players:
        json_team.show_players = True
    return json_team.json_response()

def nfl_divisions(request):
    divisions = models.NflDivision.objects.all()
    divisons_json = [nfl.JsonNflDivision(d).json_dict()
                     for d in divisions]
    return json.obj_to_json({'divisions':divisons_json})

def nfl_conferences(request):
    conferences = models.NflConference.objects.all()
    conferences_json = [nfl.JsonNflConference(c).json_dict()
                        for c in conferences]
    return json.obj_to_json({'conferences':conferences_json})

def nfl_positions(request):
    positions = models.NflPosition.objects.all()
    positions_json = [nfl.JsonNflPosition(p).json_dict()
                      for p in positions]
    return json.obj_to_json({'positions':positions_json})

def colleges(request):
    colleges = models.College.objects.all().exclude(name="Unknown")
    colleges_json = []
    for c in colleges:
        colleges_json.append(college.JsonCollege(c).json_dict())
    return json.obj_to_json({'colleges':colleges_json})

def college_players(request, id):
    c = get_object_or_404(models.College, pk=id)
    college_json = college.JsonCollege(c)
    college_json.show_players = True
    return college_json.json_response()

def my_team(request, key):
    team = get_object_or_404(models.FantasyTeam, auth_key=key)
    draft = fantasy.JsonFantasyDraft(team.draft)
    context = {
        'team': team,
        'draft': draft.json_dict(),
    }
    return render(request, 'draftHost/team_page.html', context)

def draft_page(request):
    drafts = [fantasy.JsonFantasyDraft(k).json_dict()
              for k in models.FantasyDraft.objects.all()]
    for draft in [d for d in drafts
                  if len(d['teams']) < d['team_limit']]:
        form = auth.TeamRegisterForm()
        draft['registration'] = form
    drafts.sort(key=lambda d: d['draft_start']['utc'])
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
                args = {
                    'key': team.auth_key,
                }
                private_team_page = reverse('draftHost:my_team', kwargs=args)
                return HttpResponseRedirect(private_team_page)
            else:
                return HttpResponseRedirect(reverse('draftHost:draft_page'))

        return draft_page(request)
    else:
        raise django.http.response.BadHeaderError("only POST allowed")

def documentation(request):
    return render(request, 'draftHost/documentation.html', {})
