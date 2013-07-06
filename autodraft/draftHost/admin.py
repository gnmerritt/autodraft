from draftHost.models import *
from django.contrib import admin

# Will be imported from external sources:
admin.site.register(NflTeam)
admin.site.register(Position)
admin.site.register(NflPlayer)

# Links to external DBs:
admin.site.register(ExternalDatabase)
admin.site.register(ExternalNflPlayer)

# Will be auto-generated during the draft process:
admin.site.register(FantasyUpcomingPick)
admin.site.register(FantasyPick)

# Created per-draft by the singup page:
admin.site.register(FantasyDraft)
admin.site.register(FantasyTeam)
