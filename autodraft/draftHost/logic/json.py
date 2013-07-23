import time, re
import simplejson as json
from django.http import HttpResponse


def obj_to_json(object):
    return HttpResponse(json.dumps(object), mimetype="application/json")


class JsonObject(object):
    """Super class for all other JSON objects, provides serialization.
    To add additional fields in a subclass, define one or more of
    functions, fields and mappings.
    """
    BASE_FIELDS = ['id', 'name', 'description', 'abbreviation']

    def __init__(self, db_object):
        self.db_object = db_object

    def list_to_mapping_dict(self, list):
        return {key: key for key in list}

    def eval_functions_to_dict(self, functions):
        """Checks the functions variable for a list of JSON keys
        For each key, check for a getter function, self.get_{key}()"""
        function_mapping = {}
        for key in [f for f in functions if self.is_enabled(f)]:
            func_name = "get_{f}".format(f=key)
            try:
                func = getattr(self, func_name)
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

        json_dict = self.prune_nulls(json_dict)
        json_dict = self.prune_disabled_keys(json_dict)

        return json_dict

    def prune_nulls(self, in_dict):
        """Clear any Nones / empty strings out from the JSON dictionary"""
        to_remove = [k for k,v in in_dict.iteritems()
                     if v is None or v == ""]
        for key in to_remove:
            del in_dict[key]
        return in_dict

    def prune_disabled_keys(self, in_dict):
        """Check the show_{key} boolean to see if this key is disabled"""
        to_remove = []
        for key in in_dict:
            if not self.is_enabled(key):
                to_remove.append(key)
        for key in to_remove:
            del in_dict[key]
        return in_dict

    def is_enabled(self, key):
        show_name = "show_{f}".format(f=key)
        included = not hasattr(self, show_name) or getattr(self, show_name)
        return included

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


# from http://stackoverflow.com/questions/5067218/get-utc-timestamp-in-python-with-datetime:

def utc_mktime(utc_tuple):
    """Returns number of seconds elapsed since epoch
    Note that no timezone are taken into consideration.
    utc tuple must be: (year, month, day, hour, minute, second)
    """
    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))

def datetime_to_timestamp(dt):
    """Converts a datetime object to UTC timestamp"""
    return int(utc_mktime(dt.timetuple()))


class JsonTime(JsonObject):
    """Standard time representation, input object should be a
    datetime.datetime"""
    functions = ['utc', 'str']

    def get_utc(self):
        return datetime_to_timestamp(self.db_object)

    def get_str(self):
        return unicode(self.db_object)

class EmailMasker(object):
    ADDRESS = r'.*@(.*)\.\w+'

    def __init__(self, email):
        self.email = email
        match = re.match(self.ADDRESS, (email))
        if not match or not match.group(1):
            # Don't fall back to the full email
            self.masked = "XXXX"
        else:
            self.masked = self.email.replace(match.group(1), "XXXX")
