from pymodm.errors import DoesNotExist
from rest_framework.exceptions import NotFound


def clean_mongo_dict(d):
    for k in list(d.keys()):
        if isinstance(d[k], dict):
            d[k] = clean_mongo_dict(d[k])
        elif k == '_id':
            d['id'] = str(d.pop('_id'))
        elif k == '_cls':
            d.pop('_cls')

    return d


def queryset_to_list(queryset):
    result = []
    [result.append(clean_mongo_dict(v.to_son().to_dict())) for v in queryset]
    return result


def object_to_dict(object):
    return clean_mongo_dict(object.to_son().to_dict())


def get_object_or_404(query, filters):
    try:
        return query.get(filters)
    except DoesNotExist:
        raise NotFound()
