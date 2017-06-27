from collections import deque

from behave.formatter.base import Formatter
from behave.model import ScenarioOutline

from allure_commons.logger import AllureLogger
from allure_commons.utils import uuid4
from allure_commons.utils import now

from allure_commons.model2 import TestResult
from allure_commons.model2 import TestStepResult
from allure_commons.model2 import TestBeforeResult
from allure_commons.model2 import TestResultContainer
from allure_commons.model2 import StatusDetails
from allure_commons.model2 import Status
from allure_commons.model2 import Parameter
from allure_commons.model2 import Label
from allure_commons.constants import LabelType
from allure_commons.constants import AttachmentType


STATUS = {
    'passed': Status.PASSED,
    'failed': Status.FAILED,
    'skipped': Status.SKIPPED,
    'untested': Status.BROKEN
}


def scenario_outline_parameters(feature):
    outline_parameters = {}

    def scenario_parameters(scenario_outline):
        for example in scenario_outline.examples:
            example_headings = example.table.headings
            for row in example.table:
                yield [Parameter(name=name, value=value) for name, value in zip(example_headings, row)]

    for scenario in feature.scenarios:
        if isinstance(scenario, ScenarioOutline):
            outline_parameters.update((s.name, p) for s, p in zip(scenario.scenarios, scenario_parameters(scenario)))

    return outline_parameters


class AllureFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super(AllureFormatter, self).__init__(stream_opener, config)
        report_dir = self.config.outfiles[0] if self.config.outfiles[0] else "allure-results"
        self.logger = AllureLogger(report_dir)

        self.step_queue = deque()
        self.outline_parameters = dict()

        self.current_scenario = None
        self.scenario_uuid = None
        self.group_uuid = None
        self.before_uuid = None

    def _flush_scenario(self):
        if self.group_uuid and self.before_uuid:
            self.logger.update_group(self.group_uuid, children=self.scenario_uuid)

        if self.scenario_uuid and self.current_scenario:
            status = STATUS.get(self.current_scenario.status, None)
            self.logger.update_test(self.scenario_uuid, stop=now(), status=status)
            self.logger.close_test(self.scenario_uuid)
            self.scenario_uuid, self.current_scenario = None, None

    def _attach_step_data(self, step):
        parameters = []
        if step.text:
            parameters.append(Parameter(name='text', value=step.text))
            self.logger.attach_data(uuid4(), step.text, name='.text', attachment_type=AttachmentType.TEXT)
        if step.table:
            table = [','.join(step.table.headings)]
            [table.append(','.join(list(row))) for row in step.table.rows]
            self.logger.attach_data(uuid4(), '\n'.join(table), name='.table', attachment_type=AttachmentType.CSV)

    def feature(self, feature):
        self.outline_parameters = scenario_outline_parameters(feature)

    def background(self, background):
        self.group_uuid = uuid4()
        group = TestResultContainer(uuid=self.group_uuid, name='Background')

        self.before_uuid = uuid4()
        before = TestBeforeResult(name=background.name or 'Background')

        self.logger.start_group(group.uuid, group)
        self.logger.start_before_fixture(self.group_uuid, self.before_uuid, before)

    def scenario(self, scenario):
        self._flush_scenario()
        self.current_scenario = scenario
        self.scenario_uuid = uuid4()
        labels = [Label(name=LabelType.FEATURE.value, value=scenario.feature.name)]
        parameters = self.outline_parameters.get(scenario.name, [])
        description = '\n'.join(scenario.description)

        test_case = TestResult(uuid=self.scenario_uuid,
                               start=now(),
                               name=scenario.name,
                               labels=labels,
                               description=description,
                               parameters=parameters)

        self.logger.schedule_test(self.scenario_uuid, test_case)

    def step(self, step):
        step_name = '{keyword} {title}'.format(keyword=step.keyword, title=step.name)
        parent_uuid = self.before_uuid if step in self.current_scenario.background_steps else self.scenario_uuid
        step_uuid = uuid4()
        allure_step = TestStepResult(name=step_name, start=now())

        self.logger.start_step(parent_uuid, step_uuid, allure_step)
        self._attach_step_data(step)

        self.step_queue.append(step_uuid)

    def result(self, result):
        step_uuid = self.step_queue.popleft()
        status = STATUS.get(result.status, None)
        status_details = StatusDetails(message=result.error_message) if result.error_message else None
        self.logger.stop_step(step_uuid, stop=now(), status=status, statusDetails=status_details)

    def eof(self):
        self._flush_scenario()
        if self.group_uuid and self.before_uuid:
            self.logger.stop_before_fixture(self.before_uuid)
            self.logger.stop_group(self.group_uuid)
            self.group_uuid, self.before_uuid = None, None
