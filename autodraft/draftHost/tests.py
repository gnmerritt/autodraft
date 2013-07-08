from django.test import TestCase

import draftHost.logic.objects as obj

class JsonObjectTest(TestCase):
    """Tests for the JsonObject magic"""

    def test_constructor(self):
        db_dict = {}
        json_object = obj.JsonObject(db_dict)
        self.assertFalse(json_object.d)
        self.assertEquals(json_object.db_object, db_dict)

    def test_list_to_mapping(self):
        """Tests the list to mapping function"""
        in_list = ['a', 'b', 'c']
        out_dict = obj.JsonObject({}).list_to_mapping_dict(in_list)
        for entry in in_list:
            self.assertIn(entry, out_dict)
            self.assertEquals(out_dict[entry], entry)

    def test_eval_functions_to_dict(self):
        """Verifies that the function eval-er is running correctly"""
        def getter1():
            return 1
        def getter2():
            return 2
        mapping = {
            1: getter1,
            2: getter2
        }
        output_map = obj.JsonObject({}).eval_functions_to_dict(mapping)

        for key in mapping.keys():
            self.assertIn(key, output_map)
            self.assertEquals(output_map[key], key)

    def test_json_dict_basic(self):
        pass
