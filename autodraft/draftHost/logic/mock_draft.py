import uuid

from draftHost import models

class BotTeamCreator(object):
    NAME = "AI Drafting Opponent #{}"
    EMAIL = "draftbot@blackhole.gnmerritt.net"

    def __init__(self, draft, draft_form):
        self.draft = draft
        self.num_teams = draft_form.cleaned_data['team_limit']
        self.season = models.FantasySeason.objects.filter(year="2014-2015")[0] # Eww.
        self.brain = "default"

    def run(self):
        for i in range(1, self.num_teams):
            team_data = {
                "draft": self.draft,
                "auth_key": uuid.uuid4(),
                "name": self.NAME.format(i),
                "email": self.EMAIL,
            }
            team, _ = models.FantasyTeam.objects.get_or_create(**team_data)
            bot_data = {
                "season": self.season,
                "draft": self.draft,
                "brain": self.brain,
                "team": team,
            }
            bot = models.MockDraftBot(**bot_data)
            bot.save()
