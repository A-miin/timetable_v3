
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, FieldInspector
from drf_yasg.utils import force_real_str, is_list_view
from rest_framework import exceptions, status


class ErrorResponseAutoSchema(SwaggerAutoSchema):

    def get_generic_error_schema(self):
        return openapi.Schema(
            'Generic API Error',
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'object_error': openapi.Schema(type=openapi.TYPE_STRING, description='Field where errors exists'),
                })
            },
            required=['detail']
        )

    def get_validation_error_schema(self):
        return openapi.Schema(
            'Validation Error',
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='error messages for each field that triggered a validation error. '
                                '`object_error` is for common error',
                    additional_properties=openapi.Schema(
                        title='field',
                        description='A list of error messages for the field',
                        type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),

                ),
            }
        )

    def get_response_serializers(self):
        responses = super().get_response_serializers()
        definitions = self.components.with_scope(
            openapi.SCHEMA_DEFINITIONS)  # type: openapi.ReferenceResolver

        definitions.setdefault('GenericError', self.get_validation_error_schema)
        definitions.setdefault('ValidationError', self.get_validation_error_schema)
        definitions.setdefault('APIException', self.get_validation_error_schema)

        if self.get_request_serializer() or self.get_query_serializer():
            responses.setdefault(exceptions.ValidationError.status_code, openapi.Response(
                description=force_real_str(exceptions.ValidationError.default_detail),
                schema=openapi.SchemaRef(definitions, 'ValidationError')
            ))

        security = self.get_security()
        if security is None or len(security) > 0:
            # Note: 401 error codes are coerced  into 403 see rest_framework/views.py:433:handle_exception
            # This is b/c the API uses token auth which doesn't have WWW-Authenticate header
            responses.setdefault(status.HTTP_401_UNAUTHORIZED, openapi.Response(
                description="Authentication credentials were invalid, absent or insufficient.",
                schema=openapi.SchemaRef(definitions, 'GenericError')
            ))
        if not is_list_view(self.path, self.method, self.view):
            responses.setdefault(exceptions.PermissionDenied.status_code, openapi.Response(
                description="Permission denied.",
                schema=openapi.SchemaRef(definitions, 'APIException')
            ))
            responses.setdefault(exceptions.NotFound.status_code, openapi.Response(
                description="Object does not exist or caller has insufficient permissions to access it.",
                schema=openapi.SchemaRef(definitions, 'APIException')
            ))

        return responses