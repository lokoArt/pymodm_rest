## Description
This package is inspired by Django REST Framework in order to provide a simple creation of CRUD REST API for Mongodb applications.

Some features are not implemented such as pagination and advanced serializing.
If you have any ideas how to improve this package feel free to contact me or even help me.

## How To
The main difference between DRF and this package is that this package doesn't serializers' definition. Instead, models 
are rendered automatically.

Let's say you have such Pymodm model

```
class ServiceArea(MongoModel):
    name = fields.CharField(required=True)
    price = fields.IntegerField(required=True)
    user_id = fields.IntegerField(required=True)
    geometry = fields.GeometryCollectionField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mozo'
```

In order to create CRUD api you should create a viewset

```
from api.pymodm_rest import viewsets

class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects
    instance_class = ServiceArea
    lookup_field = '_id'
``` 
Now you can use these viewset with DRF routers
```
service_router = routers.SimpleRouter()
service_router.register(r'services', mongo_views.ServiceAreaViewSet, '')
```

For real life example please check
https://github.com/lokoArt/mozo 

## Coming releases
 1) Automatic generating of CoreApi schemas
 2) Customization of serialization of fields for different methods
