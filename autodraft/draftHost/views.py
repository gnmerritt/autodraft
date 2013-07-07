from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import draftHost.logic.objects as objects
from draftHost.models import NflPlayer

def draft(request):
    return HttpResponse("draft/")

def picks(request):
    return HttpResponse("picks")

def make_pick(request, pick_id, player_id):
    return HttpResponse("picks/make/{p}/player/{who}/"
                        .format(p=pick_id, who=player_id))

def player(request, uid):
    db_player = get_object_or_404(NflPlayer, pk=uid)
    json_player = objects.JsonNflPlayer(db_player)
    return json_player.json_response()

def search(request, query):
    return HttpResponse("search/{q}".format(q=query))

def team_info(request, name):
    return HttpResponse("team/{n}".format(n=name))
