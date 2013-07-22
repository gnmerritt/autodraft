from django import forms
from draftHost import models

class AuthContext(object):
    """Fetches the current team & draft from the request"""
    def __init__(self, request):
        self.request = request
        self.find_key_from_req()
        self.find_team_from_key()
        self.find_draft_from_team()

    def find_key_from_req(self):
        self.key = self.request.GET.get('key')
        if not self.key:
            self.key = self.request.POST.get('key')

    def find_team_from_key(self):
        if self.key:
            teams = models.FantasyTeam.objects.filter(auth_key=self.key)
            if teams:
                self.team = teams[0]
                return
        self.team = None

    def find_draft_from_team(self):
        if self.team:
            self.draft = self.team.draft
        else:
            self.draft = None

    def is_valid(self):
        return self.team is not None and self.draft is not None

class TeamRegisterForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Will be obfuscated'}))
    draft_id = forms.IntegerField()
