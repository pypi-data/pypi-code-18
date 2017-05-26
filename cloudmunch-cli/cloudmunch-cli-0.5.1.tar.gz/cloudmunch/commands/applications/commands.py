# Copyright 2016 Cloudmunch Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import logging
from dateutil.parser import parse
from datetime import datetime
from cloudmunch.cli import cli
from cloudmunch.commands.applications import service
from cloudmunch import decorators, utils

@cli.group()
def applications():
    """Applications

    Commands to interact with applications that are accessbile
    for the api key used.

    The arguments for these commands can be either the name or
    the system generated id. 
    """

@applications.command('list', short_help='Lists all accessbile applications')
@decorators.timer
@decorators.response
def applications_list():
    """List all applications"""
    logging.getLogger(__name__).info('List all applications ')
    kwargs = {'application': '', 'command': 'application', 'type': utils.CommandType.LIST}
    return service.get_data(**kwargs)

@applications.command('describe', short_help='Show details for application')
@click.argument('application')
@decorators.timer
@decorators.response
def applications_describe(application):
    """Describe specified application"""
    logging.getLogger(__name__).info('Describing application %s' % (application))
    kwargs = {'application' : application, 'command': 'application', 'type': utils.CommandType.DETAILS}
    return service.get_data(**kwargs)    

@applications.command('list-tasks', short_help='Lists all the configured tasks')
@click.argument('application')
@click.option('-c', '--category', help='Task category', type=click.Choice(['build', 'build_action', 'provision', 'environment_action', 'insights', 'other']), required=False, default='insights')
@decorators.timer
@decorators.response
def applications_list_tasks(application, category):
    """List all the tasks in the application"""
    kwargs = {'application': application, 'pipeline' : '', 'category' : category, 'command': 'pipeline', 'type': utils.CommandType.LIST}
    logging.getLogger(__name__).info('List all the tasks in the applications')
    return service.get_data(**kwargs)

@applications.command('describe-task', short_help='Show details of a task')
@click.argument('application')
@click.argument('task')
@decorators.timer
@decorators.response
def applications_describe_task(application, task):
    """Describe specified application's task"""
    kwargs = {'application': application, 'pipeline' : task, 'command': 'pipeline', 'type': utils.CommandType.DETAILS}    
    logging.getLogger(__name__).info('Describing the task %s in application %s' % (task, application))
    return service.get_data(**kwargs)

@applications.command('list-runs', short_help='Lists the runs of a task')
@click.argument('application')
@click.argument('task')
@decorators.timer
@decorators.response
def applications_list_runs(application, task):
    """List the runs of a task in the application"""
    kwargs = {'application': application, 'pipeline' : task, 'run' : '', 'command': 'run', 'type': utils.CommandType.LIST}      
    logging.getLogger(__name__).info('Listing the runs for task %s in application %s' % (task, application))
    return service.get_data(**kwargs)

@applications.command('describe-run', short_help='Show details for run of a task')
@click.argument('application')
@click.argument('task')
@click.argument('run')
@decorators.timer
@decorators.response
def applications_describe_run(application, task, run):
    """Details of the run of a task in the application"""
    kwargs = {'application' : application, 'pipeline' : task, 'run' : run, 'command': 'run', 'type': utils.CommandType.DETAILS}     
    logging.getLogger(__name__).info('Listing the runs for task %s in application %s' % (task, application))
    return service.get_data(**kwargs)

@applications.command('list-integrations', short_help='Lists configured integrations')
@click.argument('application')
@decorators.timer
@decorators.response
def applications_list_integrations(application):
    """Get a list of integrations for an application"""
    kwargs = {'application': application, 'command': 'integration', 'integration': '', 'type': utils.CommandType.LIST}
    logging.getLogger(__name__).info('Listing the integrations configured in application %s ' % (application))
    return service.get_data(**kwargs)

@applications.command('describe-integration', short_help='Show details of an integration')
@click.argument('application')
@click.argument('integration')
@decorators.timer
@decorators.response
def applications_describe_integration(application, integration):
    """Get the details of an integration for an application"""
    kwargs = {'application': application, 'integration': integration, 'command': 'integration', 'type': utils.CommandType.DETAILS}
    logging.getLogger(__name__).info('Getting details of integration %s configured in application %s ' % (integration, application))
    return service.get_data(**kwargs)

@applications.command('list-resources', short_help='Lists all resources for an integration')
@click.argument('application')
@click.argument('integration')
@decorators.timer
@decorators.response
def applications_list_resources(application, integration):
    """List the resources configured for an integration in an application"""
    kwargs = {'application': application, 'integration': integration, 'resource': '', 'command': 'resource', 'type': utils.CommandType.LIST}
    logging.getLogger(__name__).info('Listing resources of integration %s configured in application %s ' % (integration, application))
    return service.get_data(**kwargs)

@applications.command('describe-resource', short_help='Show details of a configured resource')
@click.argument('application')
@click.argument('resource')
@decorators.timer
@decorators.response
def applications_describe_resource(application, resource):
    """Describe the configuration details of a resource in an application"""
    kwargs = {'application': application, 'resource': resource, 'command': 'resource', 'type': utils.CommandType.DETAILS}    
    logging.getLogger(__name__).info('Describing resource %s in application %s ' % (resource, application))
    return service.get_data(**kwargs)

def validate_date(ctx, param, value):
    """Validates entered date - can be in any format"""
    if value == '_latest':
        return value
    try:
        parsed = parse(value)
        return datetime.strftime(parsed, "%Y-%m-%d")
    except ValueError:
        raise click.BadParameter('Not a valid date')   

@applications.command('list-keymetrics', short_help='Shows all the generated key metrics for a resource')
@click.argument('application')
@click.argument('resource')
@click.option('--date', help='Date for which Key Metrics to display. If no date specified, latest key metrics will be shown', default = '_latest', required=False, callback=validate_date)
@decorators.timer
@decorators.response
def applications_list_keymetrics(application, resource, date):
    """Lists Key Metrics by date of a resource in an application"""
    #kwargs = {'application' : application, 'resource' : resource, 'insight_report': '', 'date' : date, 'key_metric' : '', 'command': 'key_metric', 'type': utils.CommandType.DETAILS}    
    kwargs = {'application' : application, 'resource' : resource, 'insight_report': date, 'key_metric' : '', 'command': 'key_metric', 'type': utils.CommandType.DETAILS}    
    logging.getLogger(__name__).info('Listing key metrics for date %s for resource %s in application %s ' % (date, resource, application))
    return service.get_data(**kwargs)

@applications.command('list-cards', short_help='Lists all the metric cards for a resources')
@click.argument('application')
@click.argument('resource')
@click.option('--date', help='Date for which Metrics to display. If no date specified, latest key metrics will be shown', default = '_latest', required=False, callback=validate_date)
@decorators.timer
@decorators.response
def applications_list_cards(application, resource, date):
    """Lists Insight Cards by date of a resource in an application"""
    kwargs = {'application' : application, 'insight_report': date, 'resource' : resource, 'insight_card' : '', 'command': 'insight_card', 'type': utils.CommandType.LIST}        
    logging.getLogger(__name__).info('Listing metrics for date %s for resource %s in application %s ' % (date, resource, application))
    return service.get_data(**kwargs) 

@applications.command('describe-card', short_help='Shows the details of a generated visualization')
@click.argument('application')
@click.argument('resource')
@click.argument('metric')
@click.option('--date', help='Date for which Metrics to display. If no date specified, latest key metrics will be shown', default = '_latest', required=False, callback=validate_date)
@decorators.timer
@decorators.response
def applications_describe_card(application, resource, metric, date):
    """Describes an Insight card by date of a resource in an application"""
    kwargs = {'application' : application, 'insight_report': date, 'resource' : resource, 'insight_card': metric, 'command': 'insight_card', 'type': utils.CommandType.DETAILS}        
    logging.getLogger(__name__).info('Showing details for date %s for metric %s for resource %s in application %s ' % (date, metric, resource, application))
    return service.get_data(**kwargs)

@applications.command('list-metrics', short_help='Shows the list of metrics for a resource')
@click.argument('application')
@click.argument('resource')
@decorators.timer
@decorators.response
def applications_list_metrics(application, resource):
    """Lists the metrics for a resource in an application"""
    kwargs = {'application' : application, 'resource' : resource, 'datastore': '', 'command': 'datastore', 'type': utils.CommandType.LIST}        
    logging.getLogger(__name__).info('List metrics for resource %s in application %s ' % (resource, application))
    return service.get_data(**kwargs)

@applications.command('show-metric-data', short_help='Shows the details of a metrics for a resource')
@click.argument('application')
@click.argument('resource')
@click.argument('metric')
@decorators.timer
@decorators.response
def applications_describe_metric(application, resource, metric):
    """Describes a metric a resource in an application"""
    kwargs = {'application' : application, 'resource' : resource, 'datastore': metric, 'command': 'extract', 'extract': '', 'type': utils.CommandType.DETAILS}        
    logging.getLogger(__name__).info('Showing details of metric %s for resource %s in application %s ' % (metric, resource, application))
    return service.get_data(**kwargs)

@applications.command('trigger-task', short_help='Triggers a task')
@click.argument('application')
@click.option('--task', help='Name of task to trigger. If none specified default task will be triggered', default = 'Insight Task', required=False)
@decorators.timer
@decorators.response
def applications_trigger_task(application, task):
    """List the runs of a task in the application"""
    kwargs = {'application': application, 'pipeline' : task, 'command': 'pipeline', 'action': 'trigger', 'data': {}, 'type': utils.CommandType.POST}      
    logging.getLogger(__name__).info('Trigger task %s in application %s' % (task, application))
    return service.post_data(**kwargs)