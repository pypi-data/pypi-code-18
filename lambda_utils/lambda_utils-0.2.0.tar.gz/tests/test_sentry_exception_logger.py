import os
import logging
from lambda_utils import sentry_expception_logger as module
from lambda_utils.sentry_expception_logger import SentryExceptionLogger
from hamcrest import assert_that, equal_to
from mock import patch


@patch.dict(os.environ, {'SENTRY_IO': 'https://key:key@app.getsentry.com/12345'})
class TestSentryExceptionLogger:
    def test_configures_logger(self):
        @SentryExceptionLogger()
        def function(event, context):
            return event

        function({'foo': 'bar'}, None)
        assert_that(len(logging.getLogger('raven').handlers), equal_to(1))

    @patch.object(module, 'Client')
    def test_set_user_context(self, client_mock):
        @SentryExceptionLogger()
        def function(event, context):
            return event

        function({'requestContext': {'authorizer': {'email': 'info@example.com'}}}, None)

        client_mock.return_value.user_context.assert_called_once_with({'email': 'info@example.com'})

    @patch.object(module, 'Client')
    def test_set_x_ray_trace_id(self, client_mock):
        @SentryExceptionLogger()
        def function(event, context):
            return event

        function({u'headers': {u'X-Amzn-Trace-Id': u'Root=1-15bfbe41663-some'}}, None)

        client_mock.return_value.tags_context.assert_called_once_with({'Request-X-Amzn-Trace-Id': u'Root=1-15bfbe41663-some'})

    @patch.object(module, 'Client')
    def test_set_x_ray_trace_id_with_cloudfront_trace_id(self, client_mock):
        @SentryExceptionLogger()
        def function(event, context):
            return event

        function({u'headers': {u'X-Amzn-Trace-Id': u'Self=1-591579e1-some;Root=1-15bfbe41663-some'}}, None)

        client_mock.return_value.tags_context.assert_called_once_with({'Request-X-Amzn-Trace-Id': u'Root=1-15bfbe41663-some'})
