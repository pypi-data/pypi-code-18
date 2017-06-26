
from click.testing import CliRunner

from check_pypi_name_cli.cli import main


def test_existing_package_exact_name_match():
    runner = CliRunner()
    result = runner.invoke(main, ['pip'])

    assert result.output == 'Normalised package name: pip is Not Available\n'
    assert result.exit_code == 0


def test_existing_package_inexact_name_match():
    runner = CliRunner()
    result = runner.invoke(main, ['Pip'])

    assert result.output == 'Normalised package name: pip is Not Available\n'
    assert result.exit_code == 0


def test_package_name_that_doesnt_exist():
    runner = CliRunner()
    result = runner.invoke(main, ['testy_mctest_case_has_cousins_who_write_pacakages'])

    assert result.output == 'Normalised package name: testy-mctest-case-has-cousins-who-write-pacakages is Available\n'
    assert result.exit_code == 0
