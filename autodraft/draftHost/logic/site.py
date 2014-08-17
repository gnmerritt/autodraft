from draftHost import models

def draft_user(request):
    draftKey = request.COOKIES.get('draftKey')
    if draftKey:
        team = models.FantasyTeam.objects.filter(auth_key=draftKey)
        if team:
            mock_drafts = models.MockDraft.objects.filter(owner=team)
            return {
                'team_name': team[0].name,
                'draftKey': draftKey,
                'mock_drafts': mock_drafts,
            }
    return {}
