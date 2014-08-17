from draftHost import models

def draft_user(request):
    draftKey = request.COOKIES.get('draftKey')
    if draftKey:
        team = models.FantasyTeam.objects.filter(auth_key=draftKey)
        if team:
            return {
                'team_name': team[0].name,
                'draftKey': draftKey
            }
    return {}
