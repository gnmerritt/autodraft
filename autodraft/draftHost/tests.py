from django.test import TestCase

from draftHost.logic.json import JsonObject

class JsonObjectTest(TestCase):
    """Tests for the JsonObject magic"""

    def test_constructor(self):
        db_dict = {}
        json_object = JsonObject(db_dict)
        self.assertEquals(json_object.db_object, db_dict)

    def test_subclass_constructor(self):
        """Verifies that python isn't playing any tricks on us re: subclasses"""
        expected = ["a", "bunch", "of", "fields"]
        class JsonSubclass(JsonObject):
            fields = expected

        subclass_dict = {'a':'b'}
        json_subclass = JsonSubclass(subclass_dict)
        self.assertEquals(json_subclass.db_object, subclass_dict)
        self.assertEquals(json_subclass.fields, expected)

    def test_list_to_mapping(self):
        """Tests the list to mapping function"""
        in_list = ['a', 'b', 'c']
        out_dict = JsonObject({}).list_to_mapping_dict(in_list)
        for entry in in_list:
            self.assertIn(entry, out_dict)
            self.assertEquals(out_dict[entry], entry)

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
            self.assertEquals(out_dict[key], key)

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
            self.assertEquals(out_dict[key], key)
