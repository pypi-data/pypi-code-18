# Copyright 2017 SrMouraSilva
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

from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.handler_utils import integer

from application.controller.banks_controller import BanksController, BankError


class SwapBankHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app
        self.controller = self.app.controller(BanksController)

    @integer('bank_a_index', 'bank_b_index')
    def put(self, bank_a_index, bank_b_index):
        try:
            banks = self.controller.banks
            bank_a = banks[bank_a_index]
            bank_b = banks[bank_b_index]

            self.controller.swap(bank_a, bank_b, self.token)

            return self.success()

        except BankError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
