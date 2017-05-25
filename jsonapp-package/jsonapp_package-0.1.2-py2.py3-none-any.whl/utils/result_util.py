from collections import OrderedDict as odict

from jsonapp.utils.dict_util import Dict


class Result(object):

    def __init__(self, success=None, data=None, error=None):

        self._success = success
        self._data = data
        self._errors = []

        if error:
            self.add_error(message=error)

    def __nonzero__(self):
        return self.success

    def __repr__(self):

        output = '<Result> {status}'.format(
            status=self.status
        )

        if self.data:
            output += ', data: {data}'.format(data=self.data)

        return output

    @property
    def success(self):
        return self._success

    @property
    def failure(self):
        return not self.success

    @property
    def failed(self):
        return not self.success

    @property
    def status(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    @property
    def errors(self):

        """
        :rtype: list of Error

        """
        return self._errors

    @property
    def errors_string(self):

        errors = []

        for error in self.errors:
            errors.append(error.odict)

        result_odict = odict()
        result_odict['errors'] = errors
        json_string = Dict(result_odict).to_pretty_json_string()
        return json_string

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def set_failed(self):

        self.success = False

    def add_error(self, message):

        error = Error(message=message)

        self.errors.append(error)

        return self

    @property
    def has_errors(self):

        if len(self.errors) > 0:
            return True

        else:
            return False

    @property
    def odict(self):

        """
        Trying to follow the jsonapi.org standard.

        """

        odict_result = odict()
        odict_result['data'] = odict()
        odict_result['data']['success'] = self.success

        if self.has_errors:
            odict_result['errors'] = []
            for error in self.errors:
                odict_result['errors'].append(error.odict)

        return odict_result


def result_success():
    result = Result(success=True)
    return result


def result_failure():
    result = Result(success=False)
    return result


class Error(object):

    def __init__(self, message):

        self._message = message

    def __str__(self):
        output = str(self.odict)
        return output

    @property
    def message(self):
        return self._message

    @property
    def odict(self):

        error_odict = odict()
        error_odict['message'] = self.message

        return error_odict
