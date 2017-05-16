# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_log import log

from almanach.api.auth import base_auth
from almanach.core import exception

LOG = log.getLogger(__name__)


class MixedAuthentication(base_auth.BaseAuth):
    def __init__(self, authentication_adapters):
        self.authentication_adapters = authentication_adapters

    def validate(self, token):
        for adapter in self.authentication_adapters:
            try:
                valid = adapter.validate(token)
                if valid:
                    LOG.debug('Validated token with adapter: %s', adapter.__class__)
                    return True
            except exception.AuthenticationFailureException:
                LOG.debug('Failed to validate with adapter: %s', adapter.__class__)
        raise exception.AuthenticationFailureException('Unable to authenticate against any authentication adapters')
