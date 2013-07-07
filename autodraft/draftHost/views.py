from django.http import HttpResponse

def draft(request):
    return HttpResponse("draft/")

def picks(request):
    return HttpResponse("picks")

def make_pick(request, pick_id, player_id):
    return HttpResponse("picks/make/{p}/player/{who}/"
                        .format(p=pick_id, who=player_id))

def player(request, uid):
    return HttpResponse("player/{uid}/".format(uid=uid))

def search(request, query):
    return HttpResponse("search/{q}".format(q=query))

def team_info(request, name):
    return HttpResponse("team/{n}".format(n=name))
