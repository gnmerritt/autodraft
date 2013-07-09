from django.http import HttpResponse
import simplejson as json

def obj_to_json(object):
    # TODO: add data/pagination objects
    return HttpResponse(json.dumps(object), mimetype="application/json")


class JsonObject(object):
    """Super class for all other JSON objects, provides serialization.
    To add additional fields in a subclass, define one or more of
    functions, fields and mappings.
    """
    BASE_FIELDS = ['id', 'name', 'description', 'abbreviation']

    def __init__(self, db_object):
        self.d = {}
        self.db_object = db_object

    def list_to_mapping_dict(self, list):
        return {key: key for key in list}

    def eval_functions_to_dict(self, functions):
        function_mapping = {}
        for key, func in functions.iteritems():
            try:
                func_value = func()
                function_mapping[key] = func_value
            except: # catch everything!
                pass
        return function_mapping

    def json_dict(self):
        json_dict = self.db_to_dict({},
                                    self.list_to_mapping_dict(self.BASE_FIELDS))
        if hasattr(self, 'fields'):
            # check the db object for any fields
            json_dict = self.db_to_dict(json_dict,
                                        self.list_to_mapping_dict(self.fields))
        if hasattr(self, 'mappings'):
            # check the db object for any mappings
            json_dict = self.db_to_dict(json_dict, self.mappings)

        if hasattr(self, 'functions'):
            # evaluate all the functions, then merge the two dictionaries
            values_from_functions = self.eval_functions_to_dict(self.functions)
            json_dict = dict(json_dict.items() + values_from_functions.items())

        return json_dict

    def json_response(self):
        json_dict = self.json_dict()
        return obj_to_json(json_dict)

    def json_string(self):
        json_dict = self.json_dict()
        return json.dumps(json_dict)

    def db_to_dict(self, json_dict, fields):
        for field, output in fields.iteritems():
            try:
                value = getattr(self.db_object, field)
                if value:
                    json_dict[output] = value
            except AttributeError:
                pass

        return json_dict
