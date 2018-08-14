"""
Generic Api Views for PyModm REST api
Inspired by http://www.django-pymodm_rest-framework.org
"""
from bson import ObjectId
from pymodm.queryset import QuerySet
from rest_framework.views import APIView

from pymodm_rest import mixins
from pymodm_rest.utils import get_object_or_404


class GenericAPIView(APIView):
    queryset = None
    instance_class = None
    lookup_field = '_id'

    def get_queryset(self):
        """
       Get the list of items for this view.
       This must be an iterable, and may be a queryset.
       Defaults to using `self.queryset`.

       This method should always be used rather than accessing `self.queryset`
       directly, as `self.queryset` gets evaluated only once, and those results
       are cached for all subsequent requests.

       You may want to override this if you need to provide different
       querysets depending on the incoming request.

       (Eg. return a list of items that is specific to the user)
       """
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.get_queryset()

        filter_kwargs = {self.lookup_field: ObjectId(self.kwargs[self.lookup_field])}
        obj = get_object_or_404(queryset, filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def filter_queryset(self, queryset):
        """
        A custom method that should be overwritten for custom filtering
        """
        return queryset


class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
