import draftHost.models as models
from django.contrib import admin

# Will be imported from external sources:
admin.site.register(models.NflConference)
admin.site.register(models.NflDivision)
admin.site.register(models.NflTeam)
admin.site.register(models.NflPosition)
admin.site.register(models.NflPlayer)
admin.site.register(models.College)

# Links to external DBs:
admin.site.register(models.ExternalDatabase)
admin.site.register(models.ExternalNflPlayer)

# Will be auto-generated during the draft process:
admin.site.register(models.FantasyPick)
admin.site.register(models.FantasySelection)

admin.site.register(models.FantasyPosition)
admin.site.register(models.FantasyRoster)
admin.site.register(models.FantasySeason)

# Created per-draft by the singup page:
admin.site.register(models.FantasyDraft)
admin.site.register(models.FantasyTeam)

# Mock drafts tie together a fantasy team & draft
admin.site.register(models.MockDraft)
admin.site.register(models.MockDraftBot)
