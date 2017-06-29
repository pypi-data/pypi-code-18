from rest_framework.schemas import SchemaGenerator
from rest_framework.compat import (
    coreapi,
    coreschema,
)

from rest_framework import schemas
from rest_framework.renderers import CoreJSONRenderer

from rest_framework_swagger import renderers


def get_swagger_view(title=None, url=None, generator_class=SchemaGenerator):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """
    return schemas.get_schema_view(
        title=title,
        url=url,
        renderer_classes=[
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer],
        generator_class=generator_class)


class CustomSchemaGenerator(SchemaGenerator):

    def get_serializer_fields(self, path, method, view):
        fields = super(CustomSchemaGenerator, self).get_serializer_fields(path, method, view)

        body_fields_absent = True if len(fields) == 0 and method in ('PUT', 'PATCH', 'POST') else False

        try:
            for param in view.query_params:
                field = coreapi.Field(
                    name=param['name'],
                    location='query',  # form
                    required=param['required'],
                    schema=coreschema.String())
                fields.append(field)
        except AttributeError:
            pass

        if body_fields_absent:
            field = coreapi.Field(
                name='data',
                location='body',  # form
                required=True,
                schema=coreschema.String())
            fields.append(field)

        return fields
