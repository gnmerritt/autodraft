from django.db import models
import datetime

class NflTeam(models.model):
    """NFL Team"""
    name = models.TextField()

class Position(models.model):
    """Football position e.g. RB or QB"""
    desc = models.TextField()
    abbreviation = models.TextField(max_length=4)

class NflPlayer(models.model):
    """Draft-eligible NFL player"""
    first_name = models.TextField()
    last_name = models.TextField()
    jersey_number = models.PositiveIntegerField()
    team = models.ForeignKey(NflTeam)
    position = models.ForeignKey(Position)

class FantasyDraft(models.model):
    name = models.TextField(max_length=20)
    admin = models.EmailField()
    draft_start = models.DateTimeField()
    time_per_pick = models.PositiveIntegerField()
    team_limit = models.PositiveIntegerField()

class FantasyTeam(models.model):
    draft = models.ForeignKey(FantasyDraft)
    name = models.TextField(max_length=80)
    email = models.EmailField()
    auth_key = models.TextField(max_length=40) # len(`uuidgen`) == 36

class FantasyUpcomingPick(models.model):
    """An upcoming pick"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    expires = models.DateTimeField('expires at')
    pick_number = models.PositiveIntegerField()

    class Meta:
        ordering = ('pick_number',)

class FantasyPick(models.model):
    """A pick that's been made"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    draft_pick = models.FantasyUpcomingPick()
    player = models.ForeignKey(NflPlayer)
    when = models.DateTimeField(default=datetime.datetime.now())
