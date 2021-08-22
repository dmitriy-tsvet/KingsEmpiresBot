import sqlalchemy.types as types
import json


class JsonDecorator(types.TypeDecorator):
    impl = types.String

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self, **kw):
        return JsonDecorator(self.impl.length)
