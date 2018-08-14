"""
Mixins for PyModm REST api
Inspired by http://www.django-pymodm_rest-framework.org
"""
from bson import ObjectId
import pymodm
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from pymodm_rest.utils import object_to_dict, queryset_to_list


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        try:
            instance = self.instance_class(**request.data)
        except ValueError as e:
            raise ValidationError(str(e.args))

        self.perform_create(instance)
        return Response(object_to_dict(instance), status=status.HTTP_201_CREATED)

    def perform_create(self, instance):
        try:
            instance.save()
        except pymodm.errors.ValidationError as e:
            raise ValidationError(str(e.message))


class ListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset_to_list(queryset)
        return Response(data)


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(object_to_dict(instance))


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        # updated object
        instance = self.get_object()
        self.perform_update(request, instance)
        return Response(object_to_dict(instance))

    def perform_update(self, request, instance):
        """
        Don't use .raw().update() as it might damage the model if non existing keys occur
        """
        for k, v in request.data.items():
            setattr(instance, k, v)

        try:
            instance.save()
        except pymodm.errors.ValidationError as e:
            raise ValidationError(str(e.message))


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
