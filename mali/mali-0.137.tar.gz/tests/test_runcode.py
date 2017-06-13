# coding=utf-8
import fudge
import httpretty
from fudge.inspector import arg

from mali import cli
from .base import BaseTest
from click.testing import CliRunner


class TestAuth(BaseTest):
    user_org = "user_org_" + BaseTest.some_random_shit()
    name = "name_" + BaseTest.some_random_shit()
    git_endpoint = "git_endpoint_" + BaseTest.some_random_shit()

    @httpretty.activate
    @fudge.patch('mali_commands.commons.handle_api')
    def test_create_runcode(self, handle_api):
        handle_api.expects_call().with_matching_args(
            arg.any(),  # ctx
            arg.any(),  # http method
            'runcode',
            {
                'name': self.name,
                'git': self.git_endpoint,
                'org': self.user_org,
            }
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["code", "create", "--org", self.user_org, "--name", self.name, "--git", self.git_endpoint],
            catch_exceptions=False)
        self.assertEquals(result.exit_code, 0)
