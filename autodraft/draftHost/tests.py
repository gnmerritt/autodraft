import datetime
from django.test import TestCase

from draftHost.logic.json import JsonObject, JsonTime
import draftHost.logic.draft as draft

class JsonObjectTest(TestCase):
    """Tests for the JsonObject magic"""

    def test_constructor(self):
        db_dict = {}
        json_object = JsonObject(db_dict)
        self.assertEqual(json_object.db_object, db_dict)

    def test_subclass_constructor(self):
        """Verifies that python isn't playing any tricks on us re: subclasses"""
        expected = ["a", "bunch", "of", "fields"]
        class JsonSubclass(JsonObject):
            fields = expected

        subclass_dict = {'a':'b'}
        json_subclass = JsonSubclass(subclass_dict)
        self.assertEqual(json_subclass.db_object, subclass_dict)
        self.assertEqual(json_subclass.fields, expected)

    def test_list_to_mapping(self):
        """Tests the list to mapping function"""
        in_list = ['a', 'b', 'c']
        out_dict = JsonObject({}).list_to_mapping_dict(in_list)
        for entry in in_list:
            self.assertIn(entry, out_dict)
            self.assertEqual(out_dict[entry], entry)

    def test_eval_functions_to_dict(self):
        """Verifies that the function eval-er is running correctly"""
        expected = ["one", "two",]
        class FuncJson(JsonObject):
            functions = expected

            def get_one(self):
                return "one"
            def get_two(self):
                return "two"

        test_obj = FuncJson({})
        out_dict = test_obj.json_dict()

        for key in expected:
            self.assertIn(key, out_dict)
            self.assertEqual(out_dict[key], key)

    def test_drop_null_values(self):
        """Make sure we drop any keys with null values"""
        class FuncJson(JsonObject):
            functions = ["none", "empty_str"]

            def get_none(self):
                return None
            def get_empty_str(self):
                return ""

        test_obj = FuncJson({})
        out_dict = test_obj.json_dict()
        self.assertEqual({}, out_dict)

    def test_skip_boolean(self):
        """Verify the show_{key} variable works and is default true"""
        class FuncJson(JsonObject):
            fields = ['one', 'two', 'three']
        class MockDb(object):
            one = "one"
            two = "two"
            three = "three"

        test_obj = FuncJson(MockDb())
        test_obj.show_one = False
        test_obj.show_two = True
        out_dict = test_obj.json_dict()

        for key in ['two', 'three']:
            self.assertIn(key, out_dict)
            self.assertEqual(out_dict[key], key)

    def test_fields_variable(self):
        class MockDb:
            def __init__(self):
                self.field1 = "field1"

        expected = ["field1"]
        class MockJson(JsonObject):
            fields = expected

        test_obj = MockJson(MockDb())
        out_dict = test_obj.json_dict()

        for key in expected:
            self.assertIn(key, out_dict)
            self.assertEqual(out_dict[key], key)


class JsonTimeTest(TestCase):
    def test_time_json(self):
        date = datetime.datetime(2008, 1, 1, 0, 0, 0, 0)
        json = JsonTime(date)
        self.assertEqual({'str': u'2008-01-01 00:00:00',
                          'utc': 1199145600},
                         json.json_dict())


class MockDbDraft(object):
    def __init__(self, num_teams):
        self.rounds = 10
        self.draft_start = 0
        self.time_per_pick = 60 # seconds


class PickAssignerTest(TestCase):
    def setUp(self):
        self.num_teams = 10
        self.mock_draft = MockDbDraft(self.num_teams)
        self.mock_draft.rounds = 3
        self.mock_draft.draft_start = 0
        self.mock_draft.time_per_pick = 120

        self.teams = range(1, self.num_teams + 1)
        self.assigner = draft.PickAssigner(self.mock_draft)
        self.assigner.teams = self.teams

        self.picks = range(1, self.num_teams * self.mock_draft.rounds + 1)

    def test_team_for_pick(self):
        round_1 = self.teams
        round_2 = range(self. num_teams, 0, -1)
        expected_picks = round_1 + round_2 + round_1

        for i, pick in enumerate(self.picks):
            expected = expected_picks[i]
            actual = self.assigner.get_team_for_pick(pick)
            self.assertEqual(expected, actual, "expected:{e}, got:{a} for pick {p}"
                              .format(e=expected, a=actual, p=pick))

    def test_time_for_pick(self):
        time_pp = self.mock_draft.time_per_pick
        expected_starts = range(0, time_pp*len(self.picks), time_pp)
        expected_expires = range(time_pp, time_pp*(len(self.picks) + 1), time_pp)

        for i, pick in enumerate(self.picks):
            start, expire = self.assigner.get_times_for_pick(pick)
            self.assertEqual(expected_starts[i], start,
                              "saw start {s} at pick {p}".format(s=start, p=pick))
            self.assertEqual(expected_expires[i], expire)
