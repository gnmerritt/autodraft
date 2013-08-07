from draftHost import models


class CollegeImporter(object):
    COLLEGE_DATA_FILE = "draftHost/data/colleges.txt"

    def build(self):
        try:
            data = open(self.COLLEGE_DATA_FILE, 'r')
            for line in data:
                parts = line.rstrip().split(',')
                college, created = models.College.objects.get_or_create(
                    id=parts[0],
                    name=parts[1],
                )
                if created:
                    print "created College {c}".format(c=college)
            data.close()
        except IOError, e:
            print "got IOError {e}".format(e=e)
