import sqlalchemy.types as types
import json


def _decode(o):
    # Note the "unicode" part is only for python2
    if isinstance(o, str):
        try:
            return int(o)
        except ValueError:
            return o
    elif isinstance(o, dict):
        return {k: _decode(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_decode(v) for v in o]
    else:
        return o


class JsonDecorator(types.TypeDecorator):
    impl = types.String

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        return json.loads(
            value,
            object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()}
        )

    def copy(self, **kw):
        return JsonDecorator(self.impl.length)
