from flask_restful import Resource, request
from app.common.exceptions import BadRequest
from app.models import UUID_LENGTH


class ServiceResource(Resource):

    @staticmethod
    def get_required_int_header(header_name):
        header_value = request.headers.get(header_name)
        if not header_value:
            raise BadRequest("'{}' is required".format(header_name))

        try:
            return int(header_value)
        except ValueError:
            raise BadRequest("'{}' expected to be integer value".format(header_name))

    @staticmethod
    def get_required_string_header(header_name):
        header_value = request.headers.get(header_name)
        if not header_value:
            raise BadRequest("'{}' is required".format(header_name))

        return header_value

    def get_company_id(self):
        return self.get_required_string_header('company-id')

    def get_application_uuid(self):
        result = self.get_required_string_header('app-uuid')
        if len(result) > UUID_LENGTH:
            raise BadRequest("Maximum length for parameter 'app-uuid' exceeded")
        return result

    def get_global_tenant_uuid(self):
        result = self.get_required_string_header('global-tenant-uuid')

        if len(result) > UUID_LENGTH:
            raise BadRequest("Maximum length for parameter 'global-tenant-uuid' exceeded")

        return result
