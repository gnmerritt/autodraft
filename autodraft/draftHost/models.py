from django.db import models
import datetime

class NflConference(models.Model):
    name = models.TextField()
    abbreviation = models.TextField(max_length=5)

    def __unicode__(self):
        return self.name

class NflDivision(models.Model):
    name = models.TextField()
    conference = models.ForeignKey(NflConference)

    def __unicode__(self):
        return self.name

class NflTeam(models.Model):
    """NFL Team"""
    name = models.TextField()
    abbreviation = models.TextField(max_length=5)
    city = models.TextField()
    division = models.ForeignKey(NflDivision)

    def __unicode__(self):
        return "{c} {n}".format(c=self.city, n=self.name)

class Position(models.Model):
    """Football position e.g. RB or QB"""
    desc = models.TextField()
    abbreviation = models.TextField(max_length=4)

    def __unicode__(self):
        return self.desc

class NflPlayer(models.Model):
    """Draft-eligible NFL player"""
    first_name = models.TextField()
    last_name = models.TextField()
    jersey_number = models.PositiveIntegerField()
    team = models.ForeignKey(NflTeam)
    position = models.ForeignKey(Position)

class ExternalDatabase(models.Model):
    """An external player DB ie ESPN or Yahoo"""
    name = models.TextField(max_length=20)
    description = models.TextField(max_length=200)
    homepage = models.URLField()

class ExternalNflPlayer(models.Model):
    """Link to an external database's player info"""
    player = models.ForeignKey(NflPlayer)
    db = models.ForeignKey(ExternalDatabase)
    external_id = models.IntegerField()
    url = models.URLField()
    picture = models.URLField()

class FantasyDraft(models.Model):
    name = models.TextField(max_length=20)
    admin = models.EmailField()
    draft_start = models.DateTimeField()
    time_per_pick = models.PositiveIntegerField()
    team_limit = models.PositiveIntegerField()

class FantasyTeam(models.Model):
    draft = models.ForeignKey(FantasyDraft)
    name = models.TextField(max_length=80)
    email = models.EmailField()
    auth_key = models.TextField(max_length=40) # len(`uuidgen`) == 36

class FantasyUpcomingPick(models.Model):
    """An upcoming pick"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    expires = models.DateTimeField('expires at')
    pick_number = models.PositiveIntegerField()

    class Meta:
        ordering = ('pick_number',)

class FantasyPick(models.Model):
    """A pick that's been made"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    when = models.DateTimeField(default=datetime.datetime.now())
    draft_pick = models.ForeignKey(FantasyUpcomingPick)
    player = models.ForeignKey(NflPlayer)
