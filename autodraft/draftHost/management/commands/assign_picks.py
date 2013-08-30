from django.core.management.base import NoArgsCommand
from draftHost.logic.draft import PickAssigner
from draftHost import models


class Command(NoArgsCommand):
    MIN_TEAMS = 4

    def handle_noargs(self, **options):
        for draft in models.FantasyDraft.objects.all():
            self.verify_draft(draft)

    def verify_draft(self, draft):
        assigner = PickAssigner(draft)
        assigner.build_teams_from_db()

        if len(assigner.teams) < self.MIN_TEAMS:
            print "Not enough teams in {draft}, returning" \
              .format(draft=str(assigner.db_draft))
            return

        status = assigner.pick_status()
        if status == 'ALL':
            print "All teams already have picks, returning"
            return
        elif status == 'SOME':
            print "Some teams have picks, need to delete all picks"
            assigner.remove_picks()

        picks = assigner.assign_picks()
        assigner.create_picks(picks)
