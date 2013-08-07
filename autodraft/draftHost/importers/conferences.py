from draftHost import models


class ConferenceImporter(object):
    """Adds the conferences to the DB"""
    CONFERENCES = [
        {"name":"National Football Conference", "abbreviation":"NFC",},
        {"name":"American Football Conference", "abbreviation":"AFC",},
    ]

    def build(self):
        for c in self.CONFERENCES:
            nfl_conference, created = models.NflConference.objects.get_or_create(**c)
