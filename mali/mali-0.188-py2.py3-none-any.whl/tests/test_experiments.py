# coding=utf-8
import requests
import fudge
import json

from fudge.inspector import arg

from click.testing import CliRunner

from tests.base import BaseCliTest
from mali import cli


class TestExperiments(BaseCliTest):
    project_id = BaseCliTest.some_random_shit_number_int63()
    experiment_id = BaseCliTest.some_random_shit_number_int63()
    user_sent_metrics = {
        BaseCliTest.some_random_shit(): BaseCliTest.some_random_shit()
    }

    @fudge.patch('mali_commands.commons.handle_api')
    def testListExperiments(self, handle_api_mock):
        handle_api_mock.expects_call().with_matching_args(
            arg.any(),  # ctx
            requests.get,
            'projects/{project_id}/experiments'.format(project_id=self.project_id)
        ).returns({
            'experiments': [
                {
                    'experiment_id': BaseCliTest.some_random_shit_number_int63(),
                    'created_at': '2017-05-04T07:18:47.620155',
                    'display_name': BaseCliTest.some_random_shit(),
                    'description': BaseCliTest.some_random_shit()
                }
            ]
        })

        runner = CliRunner()
        result = runner.invoke(cli, ['experiments', 'list', '--projectId', self.project_id], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)

    @fudge.patch('mali_commands.commons.handle_api')
    def testUpdateExperimentMetrics_withValidJSON_expectsHandleApiCallAndSuccessfulExit(self, handle_api_mock):
        handle_api_mock.expects_call().with_matching_args(
            arg.any(),  # ctx
            requests.post,
            'projects/{project_id}/experiments/{experiment_id}/metrics'.format(project_id=self.project_id,
                                                                               experiment_id=self.experiment_id),
            self.user_sent_metrics
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(cli, ['experiments', 'update_experiment_metrics', '--projectId', self.project_id,
                                     '--experimentId', self.experiment_id, '--metrics',
                                     json.dumps(self.user_sent_metrics)], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)

    @fudge.patch('mali_commands.commons.handle_api')
    def testUpdateExperimentMetrics_withValidJSONAndShortHands_expectsHandleApiCallAndSuccessfulExit(self, handle_api_mock):
        handle_api_mock.expects_call().with_matching_args(
            arg.any(),  # ctx
            requests.post,
            'projects/{project_id}/experiments/{experiment_id}/metrics'.format(project_id=self.project_id,
                                                                               experiment_id=self.experiment_id),
            self.user_sent_metrics
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(cli, ['experiments', 'update_experiment_metrics', '-p', self.project_id,
                                     '-e', self.experiment_id, '-m', json.dumps(self.user_sent_metrics)],
                               catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)

    def testUpdateExperimentMetrics_withInvalidJSON_expectsRaisingOfValueError(self):
        self.assertRaises(ValueError, CliRunner().invoke, cli, ['experiments', 'update_experiment_metrics',
                                                                '--projectId', self.project_id, '--experimentId',
                                                                self.experiment_id, '--metrics',
                                                                BaseCliTest.some_random_shit()],
                          catch_exceptions=False)

    @fudge.patch('mali_commands.commons.handle_api')
    def testUpdateModelMetrics_withValidJSON_expectsHandleApiCallAndSuccessfulExit(self, handle_api_mock):
        model_weights_hash = BaseCliTest.some_random_shit()
        handle_api_mock.expects_call().with_matching_args(
            arg.any(),  # ctx
            requests.post,
            'model_weights_hashes/{model_weights_hash}/metrics'.format(model_weights_hash=model_weights_hash),
            self.user_sent_metrics
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(cli, ['experiments', 'update_model_metrics', '--weightsHash', model_weights_hash,
                                     '--metrics', json.dumps(self.user_sent_metrics)], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
