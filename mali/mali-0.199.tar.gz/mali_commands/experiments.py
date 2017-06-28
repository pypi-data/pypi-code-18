# coding=utf-8
import click
import requests
import json

from mali_commands.commons import output_result
from mali_commands.options import project_id_option, experiment_id_option, metrics_option, model_weights_hash_option
from mali_commands.utilities.formatters import format_datetime, truncate_long_text, truncate_short_text


@click.group('experiments')
def experiments_commands():
    pass


@experiments_commands.command('list')
@project_id_option(required=True)
@click.pass_context
def list_experiments(ctx, projectid):
    """List experiments of a project.
    """
    list_experiments_path = 'projects/{project_id}/experiments'.format(project_id=projectid)
    result = ctx.obj.handle_api(ctx.obj, requests.get, list_experiments_path)
    experiments = result.get('experiments', [])

    displayed_fields = ['experiment_id', 'created_at', 'display_name', 'description']
    formatters = {
        'created_at': format_datetime,
        'display_name': truncate_short_text,
        'description': truncate_long_text,
    }
    output_result(ctx, experiments, displayed_fields, formatters=formatters)


@experiments_commands.command('update_experiment_metrics')
@project_id_option(required=True)
@experiment_id_option(required=True)
@metrics_option(required=True)
@click.pass_context
def update_experiment_metrics(ctx, projectid, experimentid, metrics):
    """Send experiment metrics to an experiment.

    Example:

    To send metrics to the 5rd experiment of the project "123", run

    \b
        mali experiments update_experiment_metrics --projectId 123 --experimentId 5 --metrics '{"ex_cost": 99}'
    """
    update_metrics_path = 'projects/{project_id}/experiments/{experiment_id}/metrics'\
        .format(project_id=projectid, experiment_id=experimentid)
    data = _get_metrics_json(metrics)

    result = ctx.obj.handle_api(ctx.obj, requests.post, update_metrics_path, data)
    output_result(ctx, result, ['ok'])


@experiments_commands.command('update_model_metrics')
@model_weights_hash_option(required=True)
@metrics_option(required=True)
@click.pass_context
def update_model_metrics(ctx, weightshash, metrics):
    """Send the model's metrics to its corresponding experiment epochs.

    Each model weights hash is attached to certain experiment epochs and thus can be used to send
    metrics that are relevant to those epochs. The model weights hash is a hexadecimal string. To
    calculate the weights hash of a model:

        - Calculate the sha1 strings of the weights for each layers

        - Calculate the sha1 string of the combine hashes. For example, the model has 3 layers with
    the layers' weight hashes: ['abc', '123', 'def'], the model weight hash is `sha1('abc123def')`

    Alternatively, you can use `missinglink-sdk` Python package to calculate the weights hash for
    your model. Each framework callback has its corresponding `get_weights_hash` method.

    WARNING: The same model weights hash can appear in different experiments or different epochs
    (for example, when running the same net twice). As such, this command will send the metrics to
    all these experiments/epochs that it can identify from the hash.

    Example:

    To send metrics of the model which hash is 324e16b5e, run

    \b
        mali experiments update_model_metrics --weightsHash 324e16b5e --metrics '{"ex_cost": 99}'

    """
    update_model_metrics_path = 'model_weights_hashes/{model_weights_hash}/metrics'\
        .format(model_weights_hash=weightshash)
    data = _get_metrics_json(metrics)

    result = ctx.obj.handle_api(ctx.obj, requests.post, update_model_metrics_path, data)
    output_result(ctx, result, ['ok'])


def _get_metrics_json(metrics_string):
    try:
        return json.loads(metrics_string)
    except ValueError:
        raise ValueError('The metrics supplied: "{metrics_supplied}" is not a valid JSON dictionary format.'
                         .format(metrics_supplied=metrics_string))
