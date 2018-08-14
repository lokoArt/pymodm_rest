import coreapi
from collections import namedtuple
from rest_framework.schemas import AutoSchema
from django.utils.six.moves.urllib import parse as urlparse

MethodField = namedtuple('Field',
                         ['name', 'required', 'location', 'schema', 'description', 'type', 'example', 'methods'])
MethodField.__new__.__defaults__ = (False, '', None, None, None, None, None)


class MongoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        fields = self.get_path_fields(path, method)
        fields += self.get_serializer_fields(path, method)
        fields += self.get_pagination_fields(path, method)
        fields += self.get_filter_fields(path, method)

        manual_fields = self.get_manual_fields(path, method)
        fields = self.update_fields(fields, manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )

    def get_manual_fields(self, path, method):
        fields = []
        for field in self._manual_fields:
            if field[7] is None or method in field[7]:
                fields.append(coreapi.Field(field[0], field[1], field[2], field[3], field[4], field[5], field[6]))

        return fields
