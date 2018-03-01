import json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return iso8601_format(obj)
        elif isinstance(obj, date):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)