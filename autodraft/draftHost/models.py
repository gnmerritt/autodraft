from django.db import models
from django.utils import timezone

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
        return u"{c} {n}".format(c=self.city, n=self.name)


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
        return u"{f} {l}".format(f=self.first_name, l=self.last_name)


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

    def __unicode__(self):
        return self.description


class FantasyDraft(models.Model):
    name = models.TextField(max_length=20)
    admin = models.EmailField()
    draft_start = models.DateTimeField()
    time_per_pick = models.PositiveIntegerField()
    team_limit = models.PositiveIntegerField()
    roster = models.ForeignKey(FantasyRoster)

    def __unicode__(self):
        return self.name

    def picks(self):
        return FantasyPick.objects.filter(fantasy_team__draft=self)

    def is_active(self, time):
        """A draft is active if any picks are active"""
        for p in self.picks():
            if p.is_active(time):
                return True
        return False


class FantasyTeam(models.Model):
    draft = models.ForeignKey(FantasyDraft)
    name = models.TextField(max_length=80)
    email = models.EmailField()
    auth_key = models.TextField(max_length=40) # len(uuid.uuid4) == 36

    def __unicode__(self):
        return self.name

    def picks(self):
        return FantasyPick.objects.filter(fantasy_team=self)

    def remove_picks(self):
        self.picks().delete()


class MockDraft(models.Model):
    """Ties together an existing fantasy team & a separate draft"""
    owner = models.ForeignKey(FantasyTeam)
    draft = models.ForeignKey(FantasyDraft)


class FantasyPick(models.Model):
    """An upcoming pick"""
    fantasy_team = models.ForeignKey(FantasyTeam)
    starts = models.DateTimeField('starts at')
    expires = models.DateTimeField('expires at')
    pick_number = models.PositiveIntegerField()

    class Meta:
        ordering = ('pick_number',)

    def __unicode__(self):
        return u"{d} - Pick {n} - {t}" \
          .format(d=self.fantasy_team.draft.name, n=self.pick_number,
                  t=self.fantasy_team.name)

    def is_active(self, time):
        """Returns whether the time is between start & expire"""
        return self.starts <= time and \
          self.expires >= time


class FantasySelection(models.Model):
    """A pick that's been made"""
    when = models.DateTimeField(default=timezone.now())
    draft_pick = models.ForeignKey(FantasyPick)
    player = models.ForeignKey(NflPlayer)
