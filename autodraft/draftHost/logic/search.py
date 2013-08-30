from django.db.models import Q
from draftHost import models
from json import JsonObject
from nfl import JsonNflPlayer


class SearchRunner(object):
    def name(self, name):
        self.name = name
        return self

    def position(self, position):
        self.position = position
        return self

    def run_search(self):
        self.query = { 'name':self.name,
                       'position':self.position, }

        players = models.NflPlayer.objects.all()

        if self.name:
            players = players.filter(
                Q(first_name__contains=self.name) |
                Q(last_name__contains=self.name)
                )

        if self.position:
            players = players.filter(
                Q(position__abbreviation__contains=self.position)
                )

        self.results = [ JsonNflPlayer(p).json_dict()
                         for p in players ]

    def json_results(self):
        self.run_search()
        print JsonSearchResults(self).json_dict()
        return JsonSearchResults(self)


class JsonSearchResults(JsonObject):
    fields = ['results', 'query']
    show_name = False
