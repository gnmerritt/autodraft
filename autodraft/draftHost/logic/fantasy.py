from json import JsonObject

class JsonFantasyTeam(JsonObject):
    fields = ['name', 'email']

    def __init__(self, db_fantasy_team):
        super(JsonFantasyTeam, self).__init__(db_fantasy_team)
        self.functions = {
            'picks': self.get_picks,
            'draft': self.get_draft,
        }

    def get_picks(self):
        return "TODO"

    def get_draft(self):
        return "TODO"
