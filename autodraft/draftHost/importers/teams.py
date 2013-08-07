import simplejson as json

from draftHost import models


class TeamImporter(object):
    TEAM_DATA_FILE = "draftHost/data/teams.json"

    def __init__(self):
        self.json = self.load_json()

    def load_json(self):
        try:
            json_file = open(self.TEAM_DATA_FILE, 'r')
            data = json.load(json_file)
            return data
        except IOError, e:
            print "got error {e}".format(e=e)
            return None

    def build(self):
        for conference_abbr, data in self.json.iteritems():
            conference = models.NflConference.objects.get(abbreviation=conference_abbr)

            for division_name, teams in data.iteritems():
                division, created_division = models.NflDivision.objects.get_or_create(
                    conference=conference,
                    name="{c} {d}".format(c=conference_abbr, d=division_name))

                for team in teams:
                    self.add_team(division, team)

    def add_team(self, division, team_data):
        team_data['division'] = division
        team_data['abbreviation'] = 'TODO'
        team, created = models.NflTeam.objects.get_or_create(**team_data)
        self.add_defense(team)
        if created:
            print "adding {t} to {d}".format(t=team_data, d=division.name)

    def add_defense(self, team):
        fantasy_defense = models.FantasyPosition.objects \
          .filter(position__abbreviation="DST")[0]
        college, _ = models.College.objects.get_or_create(name="Unknown")
        if fantasy_defense:
            defense_player = {
                'position': fantasy_defense.position,
                'fantasy_position': fantasy_defense,
                'first_name': 'Defense/Special Teams',
                'last_name': unicode(team),
                'team':team,
                'school': college,
            }
            _, created = models.NflPlayer.objects.get_or_create(**defense_player)
            if created:
                print "added fantasy_defense for {t}".format(t=unicode(team))
        else:
            print "need to import positions in order to add defenses"
