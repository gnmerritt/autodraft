from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone

from draftHost import models

def team_from_request(request):
    draftKey = request.COOKIES.get('draftKey')
    if draftKey:
        team = models.FantasyTeam.objects.filter(auth_key=draftKey)
        if team:
            return team[0], draftKey
    return None, draftKey

def draft_user(request):
    team, draftKey = team_from_request(request)
    if team:
        mock_drafts = models.MockDraft.objects.filter(owner=team)
        return {
            'team_name': team.name,
            'draftKey': draftKey,
            'mock_drafts': mock_drafts,
        }
    return {}


class MockDraftForm(forms.ModelForm):
    """Form for creating a new FantasyDraft"""
    name = forms.CharField(initial="ignored", widget=forms.HiddenInput())
    admin = forms.EmailField(initial="mockdrafts@blackhole.gnmerritt.net",
                             widget=forms.HiddenInput())
    draft_start = forms.DateTimeField(
        validators=[MinValueValidator(timezone.now())],
        input_formats=["%m/%d/%Y %I:%M:%S %p"])
    team_limit = forms.IntegerField(initial=12,
                                    validators=[MinValueValidator(4)])
    time_per_pick = forms.IntegerField(initial=10,
                                       validators=[MinValueValidator(5)])

    class Meta:
        model = models.FantasyDraft
        fields = ['name', 'admin', 'draft_start', 'time_per_pick',
                  'team_limit', 'roster']

    def clean_name(self):
        draft_num = models.MockDraft.objects.all().count() + 1
        return "Autodraft Mock Draft #{}".format(draft_num)
