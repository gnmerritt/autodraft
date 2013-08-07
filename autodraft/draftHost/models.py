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


class NflPosition(models.Model):
    """Football position e.g. RB, QB, S"""
    description = models.TextField()
    abbreviation = models.TextField(max_length=4)

    def __unicode__(self):
        return self.description


class FantasyPosition(models.Model):
    """Fantasy position - a simple subset of NflPositions"""
    position = models.ForeignKey(NflPosition)

    def __unicode__(self):
        return unicode(self.position)

class College(models.Model):
    """A NCAA College"""
    name = models.TextField(max_length=30)

    def __unicode__(self):
        return self.name

class NflPlayer(models.Model):
    """Draft-eligible NFL player"""
    first_name = models.TextField()
    last_name = models.TextField()
    draft_year = models.PositiveIntegerField(default=1)
    team = models.ForeignKey(NflTeam)
    school = models.ForeignKey(College)
    position = models.ForeignKey(NflPosition)
    fantasy_position = models.ForeignKey(FantasyPosition)

    def __unicode__(self):
        return "{f} {l}".format(f=self.first_name, l=self.last_name)


class ExternalDatabase(models.Model):
    """An external player DB ie ESPN or Yahoo"""
    name = models.TextField(max_length=20)
    description = models.TextField(max_length=200)
    homepage = models.URLField()

    def __unicode__(self):
        return self.name


class ExternalNflPlayer(models.Model):
    """Link to an external database's player info"""
    player = models.ForeignKey(NflPlayer)
    db = models.ForeignKey(ExternalDatabase)
    external_id = models.IntegerField()
    url = models.URLField()
    picture = models.URLField()


class ExternalNflTeam(models.Model):
    """Link to an external database's team info"""
    team = models.ForeignKey(NflTeam)
    db = models.ForeignKey(ExternalDatabase)
    external_id = models.IntegerField()
    url = models.URLField()


class FantasyRoster(models.Model):
    description = models.TextField() ## TODO: this should be more than a text field?
    slots = models.PositiveIntegerField()


class FantasyDraft(models.Model):
    name = models.TextField(max_length=20)
    admin = models.EmailField()
    draft_start = models.DateTimeField()
    time_per_pick = models.PositiveIntegerField()
    team_limit = models.PositiveIntegerField()
    roster = models.ForeignKey(FantasyRoster)

    def __unicode__(self):
        return self.name


class FantasyTeam(models.Model):
    draft = models.ForeignKey(FantasyDraft)
    name = models.TextField(max_length=80)
    email = models.EmailField()
    auth_key = models.TextField(max_length=40) # len(uuid.uuid4) == 36

    def __unicode__(self):
        return self.name


class FantasyPick(models.Model):
    """An upcoming pick"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    starts = models.DateTimeField('starts at')
    expires = models.DateTimeField('expires at')
    pick_number = models.PositiveIntegerField()

    class Meta:
        ordering = ('pick_number',)


class FantasySelection(models.Model):
    """A pick that's been made"""
    when = models.DateTimeField(default=datetime.datetime.now())
    draft_pick = models.ForeignKey(FantasyPick)
    player = models.ForeignKey(NflPlayer)
