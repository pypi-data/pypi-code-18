# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


"""
Realtime services functions.

"""

from __future__ import print_function

import getopt
import json
import os
import os.path
import subprocess
import time

import requests
import tabulate
import yaml
from builtins import input #pylint: disable=redefined-builtin
from kubernetes.client.rest import ApiException
from pkg_resources import resource_string

from ._docker_utils import check_docker_credentials
from ._docker_utils import get_docker_client
from ._realtimeutilities import get_sample_data
from ._realtimeutilities import resolve_marathon_base_url
from .._k8s_util import KubernetesOperations
from .._k8s_util import check_for_kubectl
from .._k8s_util import get_k8s_frontend_url
from .._util import Constants
from .._util import cli_context
from .._util import create_docker_image
from .._util import get_json
from .._util import is_int

from kubernetes.client.rest import ApiException
from ...ml import __version__
from .._constants import SUCCESS_RETURN_CODE
from .._constants import USER_ERROR_RETURN_CODE
from .._constants import SYSTEM_ERROR_RETURN_CODE

# Local mode functions


def realtime_service_delete_local(service_name, verbose):
    """Delete a locally published realtime web service."""
    client = get_docker_client()
    containers = client.containers.list(filters={'label': 'amlid={}'.format(service_name)})
    if not containers:
        print("[Local mode] Error: no service named {} running locally.".format(service_name))
        print("[Local mode] To delete a cluster based service, switch to remote mode first: az ml env remote")
        return
    if len(containers) != 1:
        print("[Local mode] Error: ambiguous reference - too many containers ({}) with the same label.".format(
            len(containers)))
        return
    container = containers[0]
    container_id = container.attrs['Id'][0:12]
    if verbose:
        print("Killing docker container id {}".format(container_id))
    image_name = container.attrs['Config']['Image']
    container.kill()
    container.remove()
    client.images.remove(image_name, force=True)
    print("Service deleted.")
    return SUCCESS_RETURN_CODE


def get_local_realtime_service_port(service_name, verbose):
    """Find the host port mapping for a locally published realtime web service."""

    try:
        dockerps_output = subprocess.check_output(
            ["docker", "ps", "--filter", "label=amlid={}".format(service_name)]).decode('ascii').rstrip().split("\n") #pylint: disable=line-too-long
    except subprocess.CalledProcessError:
        return -1
    if verbose:
        print("docker ps:")
        print(dockerps_output)
    if len(dockerps_output) == 1:
        return -1
    elif len(dockerps_output) == 2:
        container_id = dockerps_output[1][0:12]
        container_ports = subprocess.check_output(["docker", "port", container_id]).decode('ascii').strip().split('\n')
        container_ports_dict = dict(map((lambda x: tuple(filter(None, x.split('->')))), container_ports))
        # 5001 is the port we expect an ICE-built container to be listening on
        matching_ports = list(filter(lambda k: '5001' in k, container_ports_dict.keys()))
        if matching_ports is None or len(matching_ports) != 1:
            return -2
        container_port = container_ports_dict[matching_ports[0]].split(':')[1].rstrip()
        if verbose:
            print("Container port: {}".format(container_port))
        return container_port
    else:
        return -2


def realtime_service_deploy_local(context, image, verbose, app_insights_enabled):
    """Deploy a realtime web service locally as a docker container."""

    print("[Local mode] Running docker container.")
    service_label = image.split("/")[1]

    # Delete any local containers with the same label
    existing_container_port = get_local_realtime_service_port(service_label, verbose)
    if is_int(existing_container_port) and int(existing_container_port) > 0:
        print('Found existing local service with the same name running at http://127.0.0.1:{}/score'
              .format(existing_container_port))
        answer = context.get_input('Delete existing service and create new service (y/N)? ')
        answer = answer.rstrip().lower()
        if answer != 'y' and answer != 'yes':
            print('Canceling service create.')
            return 1
        realtime_service_delete_local(service_label, verbose)

    # Check if credentials to the ACR are already configured in ~/.docker/config.json
    check_docker_credentials(context.acr_home, context.acr_user, context.acr_pw, verbose)

    try:
        subprocess.check_call(['docker', 'pull', image])
        docker_output = subprocess.check_output(
            ["docker", "run", "-e", "AML_APP_INSIGHTS_KEY={}".format(context.app_insights_account_key),
                              "-e", "AML_APP_INSIGHTS_ENABLED={}".format(app_insights_enabled),
                              "-d", "-P", "-l", "amlid={}".format(service_label), "{}".format(image)]).decode('ascii')
    except subprocess.CalledProcessError:
        print('[Local mode] Error starting docker container. Please ensure you have permissions to run docker.')
        return

    try:
        dockerps_output = subprocess.check_output(["docker", "ps"]).decode('ascii').split("\n")[1:]
    except subprocess.CalledProcessError:
        print('[Local mode] Error starting docker container. Please ensure you have permissions to run docker.')
        return

    container_created = (x for x in dockerps_output if x.startswith(docker_output[0:12])) is not None
    if container_created:
        dockerport = get_local_realtime_service_port(service_label, verbose)
        if int(dockerport) < 0:
            print('[Local mode] Failed to start container. Please report this to deployml@microsoft.com with your image id: {}'.format(image)) #pylint: disable=line-too-long
            return

        sample_data_available = get_sample_data('http://127.0.0.1:{}/sample'.format(dockerport), None, verbose)
        input_data = "'{{\"input\":\"{}\"}}'"\
            .format(sample_data_available if sample_data_available else '!! YOUR DATA HERE !!')
        print("[Local mode] Success.")
        print('[Local mode] Scoring endpoint: http://127.0.0.1:{}/score'.format(dockerport))
        print("[Local mode] Usage: az ml service run realtime -n " + service_label + " [-d {}]".format(input_data))
        return SUCCESS_RETURN_CODE
    else:
        print("[Local mode] Error creating local web service. Docker failed with:")
        print(docker_output)
        print("[Local mode] Please help us improve the product by mailing the logs to ritbhat@microsoft.com")
        return


def realtime_service_run_local(service_name, input_data, verbose):
    """Run a previously published local realtime web service."""

    container_port = get_local_realtime_service_port(service_name, verbose)
    if is_int(container_port) and int(container_port) < 0:
        print("[Local mode] No service named {} running locally.".format(service_name))
        print("To run a remote service, switch environments using: az ml env remote")
        return
    else:
        headers = {'Content-Type': 'application/json'}
        if input_data == '':
            print("No input data specified. Checking for sample data.")
            sample_url = 'http://127.0.0.1:{}/sample'.format(container_port)
            sample_data = get_sample_data(sample_url, headers, verbose)
            input_data = '{{"input":"{}"}}'.format(sample_data)
            if not sample_data:
                print(
                    "No sample data available. To score with your own data, run: az ml service run realtime -n {} -d <input_data>" #pylint: disable=line-too-long
                    .format(service_name))
                return
            print('Using sample data: ' + input_data)
        else:
            if verbose:
                print('[Debug] Input data is {}'.format(input_data))
                print('[Debug] Input data type is {}'.format(type(input_data)))
            try:
                json.loads(input_data)
            except ValueError:
                print('[Local mode] Invalid input. Expected data of the form \'{{"input":"[[val1,val2,...]]"}}\'')
                print('[Local mode] If running from a shell, ensure quotes are properly escaped.')
                return

        service_url = 'http://127.0.0.1:{}/score'.format(container_port)
        if verbose:
            print("Service url: {}".format(service_url))
        try:
            result = requests.post(service_url, headers=headers, data=input_data, verify=False)
        except requests.ConnectionError:
            print('[Local mode] Error connecting to container. Please try recreating your local service.')
            return

        if verbose:
            print(result.content)

        if result.status_code == 200:
            result = result.json()
            print(result['result'])
            return SUCCESS_RETURN_CODE
        else:
            print(result.content)

# Cluster mode functions


def realtime_service_scale(service_name, num_replicas, context=cli_context):
    _realtime_service_scale(service_name, num_replicas, context)


def _realtime_service_scale(service_name, num_replicas, context=cli_context):
    """Scale a published realtime web service."""
    if context.in_local_mode():
        print("Error: Scaling is not supported in local mode.")
        print("To scale a cluster based service, switch to cluster mode first: az ml env cluster")
        return SUCCESS_RETURN_CODE

    elif context.env_is_k8s:
        try:
            if num_replicas < 1 or num_replicas > 17:
                raise ValueError
        except ValueError:
            print("The -z option must be an integer in range [1-17] inclusive.")
            return

        ops = KubernetesOperations()
        ops.scale_deployment(service_name, num_replicas)
        return SUCCESS_RETURN_CODE

    if service_name == '':
        print("Error: missing service name.")
        print("az ml service scale realtime -n <service name> -c <instance_count>")
        return

    if num_replicas < 0 or num_replicas > 5:
        print("Error: instance count must be between 1 and 5.")
        print("To delete a service, use: az ml service delete")
        return USER_ERROR_RETURN_CODE

    headers = {'Content-Type': 'application/json'}
    data = {'instances': num_replicas}
    marathon_base_url = resolve_marathon_base_url(context)
    if marathon_base_url is None:
        return
    marathon_url = marathon_base_url + '/marathon/v2/apps'
    success = False
    tries = 0
    print("Scaling service.", end="")
    start = time.time()
    scale_result = requests.put(marathon_url + '/' + service_name, headers=headers, data=json.dumps(data), verify=False)
    if scale_result.status_code != 200:
        print('Error scaling application.')
        print(scale_result.content)
        return

    try:
        scale_result = scale_result.json()
    except ValueError:
        print('Error scaling application.')
        print(scale_result.content)
        return

    if 'deploymentId' in scale_result:
        print("Deployment id: " + scale_result['deploymentId'])
    else:
        print('Error scaling application.')
        print(scale_result.content)
        return

    m_app = requests.get(marathon_url + '/' + service_name)
    m_app = m_app.json()
    while 'deployments' in m_app['app']:
        if not m_app['app']['deployments']:
            success = True
            break
        if int(time.time() - start) > 60:
            break
        tries += 1
        if tries % 5 == 0:
            print(".", end="")
        m_app = requests.get(marathon_url + '/' + service_name)
        m_app = m_app.json()

    print("")

    if not success:
        print("  giving up.")
        print("There may not be enough capacity in the cluster. Please try deleting or scaling down other services first.") #pylint: disable=line-too-long
        return

    print("Successfully scaled service to {} instances.".format(num_replicas))
    return SUCCESS_RETURN_CODE


def realtime_service_delete_kubernetes(context, service_name, verbose):
    k8s_ops = KubernetesOperations()
    try:
        if not check_for_kubectl(context):
            print('')
            print('kubectl is required to delete webservices. Please install it on your path and try again.')
            return
        k8s_ops.delete_service(service_name)
        k8s_ops.delete_deployment(service_name)
        return SUCCESS_RETURN_CODE
    except ApiException as exc:
        if exc.status == 404:
            print("Unable to find web service with name {}.".format(service_name))
            return
        print("Exception occurred while trying to delete service {}. {}".format(service_name, exc))


def realtime_service_delete(service_name, verb, context=cli_context):
    _realtime_service_delete(service_name, verb, context)


def _realtime_service_delete(service_name, verb, context=cli_context):
    """Delete a realtime web service."""

    verbose = verb

    if context.in_local_mode():
        return realtime_service_delete_local(service_name, verbose)

    response = context.get_input("Permanently delete service {} (y/N)? ".format(service_name))
    response = response.rstrip().lower()
    if response != 'y' and response != 'yes':
        return

    if context.env_is_k8s:
        return realtime_service_delete_kubernetes(context, service_name, verbose)

    if context.acs_master_url is None:
        print("")
        print("Please set up your ACS cluster for AML. See 'az ml env about' for more information.")
        return

    headers = {'Content-Type': 'application/json'}
    marathon_base_url = resolve_marathon_base_url(context)
    marathon_url = marathon_base_url + '/marathon/v2/apps'
    try:
        delete_result = requests.delete(marathon_url + '/' + service_name, headers=headers, verify=False)
    except requests.ConnectTimeout:
        print('Error: timed out trying to establish a connection to ACS. Please check that your ACS is up and healthy.')
        print('For more information about setting up your environment, see: "az ml env about".')
        return
    except requests.ConnectionError:
        print('Error: Could not establish a connection to ACS. Please check that your ACS is up and healthy.')
        print('For more information about setting up your environment, see: "az ml env about".')
        return

    if delete_result.status_code != 200:
        print('Error deleting service: {}'.format(delete_result.content))
        return

    try:
        delete_result = delete_result.json()
    except ValueError:
        print('Error deleting service: {}'.format(delete_result.content))
        return

    if 'deploymentId' not in delete_result:
        print('Error deleting service: {}'.format(delete_result.content))
        return

    print("Deployment id: " + delete_result['deploymentId'])
    m_app = requests.get(marathon_url + '/' + service_name)
    m_app = m_app.json()
    transient_error_count = 0
    while ('app' in m_app) and ('deployments' in m_app['app']):
        if not m_app['app']['deployments']:
            break
        try:
            m_app = requests.get(marathon_url + '/' + service_name)
        except (requests.ConnectionError, requests.ConnectTimeout):
            if transient_error_count < 3:
                print('Error: lost connection to ACS cluster. Retrying...')
                continue
            else:
                print('Error: too many retries. Giving up.')
                return
        m_app = m_app.json()

    print("Deleted.")
    return SUCCESS_RETURN_CODE


def realtime_service_create(score_file, dependencies, requirements, schema_file, service_name,
                            verb, custom_ice_url, target_runtime, app_insights_logging_enabled, model, num_replicas,
                            context=cli_context):
    _realtime_service_create(score_file, dependencies, requirements, schema_file, service_name,
                            verb, custom_ice_url, target_runtime, app_insights_logging_enabled, model, num_replicas,
                            context)


def _realtime_service_create(score_file, dependencies, requirements, schema_file, service_name,
                            verb, custom_ice_url, target_runtime, app_insights_logging_enabled, model, num_replicas,
                            context=cli_context):
    """Create a new realtime web service."""
    image = create_docker_image(score_file, dependencies, service_name, verb, target_runtime, context, requirements,
                                schema_file, model, custom_ice_url)

    if image is None:
        return

    app_insights_enabled = str(app_insights_logging_enabled).lower()
    if context.in_local_mode():
        return realtime_service_deploy_local(context, image, verb, app_insights_enabled)
    elif context.env_is_k8s:
        return realtime_service_deploy_k8s(context, image, service_name, app_insights_enabled,  num_replicas, verb)
    else:
        return realtime_service_deploy(context, image, service_name, app_insights_enabled, verb)


def realtime_service_deploy(context, image, app_id, app_insights_enabled, verbose):
    """Deploy a realtime web service from a docker image."""

    marathon_app = resource_string(__name__, 'data/marathon.json')
    marathon_app = json.loads(marathon_app.decode('ascii'))
    marathon_app['container']['docker']['image'] = image
    marathon_app['labels']['HAPROXY_0_VHOST'] = context.acs_agent_url
    marathon_app['labels']['AMLID'] = app_id
    marathon_app['env']['AML_APP_INSIGHTS_KEY'] = context.app_insights_account_key
    marathon_app['env']['AML_APP_INSIGHTS_ENABLED'] = app_insights_enabled
    marathon_app['id'] = app_id

    if verbose:
        print('Marathon payload: {}'.format(marathon_app))

    headers = {'Content-Type': 'application/json'}
    marathon_base_url = resolve_marathon_base_url(context)
    marathon_url = marathon_base_url + '/marathon/v2/apps'
    try:
        deploy_result = requests.put(
            marathon_url + '/' + app_id, headers=headers, data=json.dumps(marathon_app), verify=False)
    except requests.exceptions.ConnectTimeout:
        print('Error: timed out trying to establish a connection to ACS. Please check that your ACS is up and healthy.')
        print('For more information about setting up your environment, see: "az ml env about".')
        return
    except requests.ConnectionError:
        print('Error: Could not establish a connection to ACS. Please check that your ACS is up and healthy.')
        print('For more information about setting up your environment, see: "az ml env about".')
        return

    try:
        deploy_result.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        print('Error creating service: {}'.format(ex))
        return

    try:
        deploy_result = get_json(deploy_result.content)
    except ValueError:
        print('Error creating service.')
        print(deploy_result.content)
        return

    print("Deployment id: " + deploy_result['deploymentId'])
    m_app = requests.get(marathon_url + '/' + app_id)
    m_app = m_app.json()
    while 'deployments' in m_app['app']:
        if not m_app['app']['deployments']:
            break
        m_app = requests.get(marathon_url + '/' + app_id)
        m_app = m_app.json()

    print("Success.")
    print("Usage: az ml service run realtime -n " + app_id + " [-d '{\"input\":\"!! YOUR DATA HERE !!\"}']")
    return SUCCESS_RETURN_CODE


def realtime_service_deploy_k8s(context, image, app_id, app_insights_enabled, num_replicas, verbose=False):
    """Deploy a realtime Kubernetes web service from a docker image."""

    k8s_template_path = os.path.join(Constants.SERVICE_DATA_DIRECTORY, 'kubernetes_deployment_template.yaml')
    k8s_service_template_path = os.path.join(Constants.SERVICE_DATA_DIRECTORY, 'kubernetes_service_template.yaml')
    num_replicas = int(num_replicas)

    try:
        with open(k8s_template_path) as f:
            kubernetes_app = yaml.load(f)
    except OSError as exc:
        print("Unable to find kubernetes deployment template file.".format(exc))
        raise
    kubernetes_app['metadata']['name'] = app_id + '-deployment'
    kubernetes_app['spec']['replicas'] = num_replicas
    kubernetes_app['spec']['template']['spec']['containers'][0]['image'] = image
    kubernetes_app['spec']['template']['spec']['containers'][0]['name'] = app_id
    kubernetes_app['spec']['template']['metadata']['labels']['webservicename'] = app_id
    kubernetes_app['spec']['template']['metadata']['labels']['azuremlappname'] = app_id
    kubernetes_app['spec']['template']['metadata']['labels']['type'] = "realtime"
    kubernetes_app['spec']['template']['spec']['containers'][0]['env'][0]['value'] = context.app_insights_account_key
    kubernetes_app['spec']['template']['spec']['containers'][0]['env'][1]['value'] = app_insights_enabled
    kubernetes_app['spec']['template']['spec']['imagePullSecrets'][0]['name'] = context.acr_user + 'acrkey'

    k8s_ops = KubernetesOperations()
    timeout_seconds = 1200
    try:
        k8s_ops.deploy_deployment(kubernetes_app, timeout_seconds, num_replicas, context.acr_user + 'acrkey', verbose)
        k8s_ops.create_service(k8s_service_template_path, app_id, 'realtime', verbose)

        print("Success.")
        print("Usage: az ml service run realtime -n " + app_id + " [-d '{\"input\":\"!! YOUR DATA HERE !!\"}']")
        return SUCCESS_RETURN_CODE
    except ApiException as exc:
        print("An exception occurred while deploying the service. {}".format(exc))


def realtime_service_view(service_name, verb=False, context=cli_context):
    _realtime_service_view(service_name, verb, context)


def _realtime_service_view(service_name, verb=False, context=cli_context):
    """View details of a previously published realtime web service."""

    verbose = verb

    # First print the list view of this service
    num_services = get_webservices(service_name, verb, context)

    scoring_url = None
    usage_headers = ['-H "Content-Type:application/json"']
    default_sample_data = '!!!YOUR DATA HERE !!!'

    if context.in_local_mode():
        client = get_docker_client()
        containers = client.containers.list(filters={'label': 'amlid={}'.format(service_name)})
        if len(containers) != 1:
            print('[Local mode] Error retrieving container details.')
            print('[Local mode] Label should match exactly one container '
                  'and instead matched {}.'.format(len(containers)))
            return
        container = containers[0]
        ports = container.attrs['NetworkSettings']['Ports']
        scoring_port_key = [x for x in ports.keys() if '5001' in x]
        if len(scoring_port_key) != 1:
            print('[Local mode] Error: Malconfigured container. '
                  'Cannot determine scoring port.')
            return
        scoring_port = ports[scoring_port_key[0]][0]['HostPort']
        if scoring_port:
            scoring_url = 'http://127.0.0.1:' + str(scoring_port) + '/score'

            # Try to get the sample request from the container
            sample_url = 'http://127.0.0.1:' + str(scoring_port) + '/sample'
            headers = {'Content-Type': 'application/json'}
        else:
            print('[Local mode] Error: Misconfigured container. '
                  'Cannot determine scoring port.')
            return
    else:
        if context.env_is_k8s:
            try:
                fe_url = get_k8s_frontend_url()
            except ApiException:
                return
            scoring_url = fe_url + service_name + '/score'
            sample_url = fe_url + service_name + '/sample'
            headers = {'Content-Type': 'application/json'}
        else:
            if context.acs_agent_url is not None:
                scoring_url = 'http://' + context.acs_agent_url + ':9091/score'
                sample_url = 'http://' + context.acs_agent_url + ':9091/sample'
                headers = {'Content-Type': 'application/json', 'X-Marathon-App-Id': "/{}".format(service_name)}
                usage_headers.append('-H "X-Marathon-App-Id:/{}"'.format(service_name))
            else:
                print('Unable to determine ACS Agent URL. '
                      'Please ensure that AML_ACS_AGENT environment variable is set.')
                return

    service_sample_data = get_sample_data(sample_url, headers, verbose)
    sample_data = '{{"input":"{}"}}'.format(
        service_sample_data if service_sample_data is not None else default_sample_data)
    if num_services:
        print('Usage:')
        print('  az ml  : az ml service run realtime -n {} [-d \'{}\']'.format(service_name, sample_data))
        print('  curl : curl -X POST {} --data \'{}\' {}'.format(' '.join(usage_headers), sample_data, scoring_url))
        return SUCCESS_RETURN_CODE


def realtime_service_list(service_name=None, verb=False, context=cli_context):
    _realtime_service_list(service_name, verb, context)


def _realtime_service_list(service_name=None, verb=False, context=cli_context):
    # all error paths return None--if we get anything that is not None, return SUCCESS
    return SUCCESS_RETURN_CODE if get_webservices(service_name, verb, context) is not None else None


def get_webservices(service_name=None, verb=False, context=cli_context):
    """List published realtime web services."""

    verbose = verb

    if context.in_local_mode():
        if service_name is not None:
            filters = {'label': 'amlid={}'.format(service_name)}
        else:
            filters = {'label': 'amlid'}

        client = get_docker_client()

        app_table = [
                        ['NAME', 'IMAGE', 'CPU', 'MEMORY', 'STATUS', 'INSTANCES',
                         'HEALTH']
                    ] + [[
                             container.attrs['Config']['Labels']['amlid'],
                             container.attrs['Config'][
                                 'Image'] if 'Image' in container.attrs else 'Unknown',
                             'N/A',  # CPU
                             'N/A',  # Memory
                             container.attrs['State']['Status'],
                             1,  # Instances
                             'N/A',  # health
                         ] for container in client.containers.list(filters=filters)
                         ]

        print(tabulate.tabulate(app_table, headers='firstrow', tablefmt='psql'))

        return len(app_table) - 1
    # Cluster mode
    if context.env_is_k8s:
        return realtime_service_list_kubernetes(context, service_name, verbose)

    if service_name is not None:
        extra_filter_expr = ", AMLID=={}".format(service_name)
    else:
        extra_filter_expr = ""

    marathon_base_url = resolve_marathon_base_url(context)
    if not marathon_base_url:
        return
    marathon_url = marathon_base_url + '/marathon/v2/apps?label=AMLBD_ORIGIN' + extra_filter_expr
    if verbose:
        print(marathon_url)
    try:
        list_result = requests.get(marathon_url)
    except requests.ConnectionError:
        print('Error connecting to ACS. Please check that your ACS cluster is up and healthy.')
        return
    try:
        apps = list_result.json()
    except ValueError:
        print('Error retrieving apps from ACS. Please check that your ACS cluster is up and healthy.')
        print(list_result.content)
        return

    if 'apps' in apps and len(apps['apps']) > 0:
        app_table = [['NAME', 'IMAGE', 'CPU', 'MEMORY', 'STATUS', 'INSTANCES', 'HEALTH']]
        for app in apps['apps']:
            if 'container' in app and 'docker' in app['container'] and 'image' in app['container']['docker']:
                app_image = app['container']['docker']['image']
            else:
                app_image = 'Unknown'
            app_entry = [app['id'].strip('/'), app_image, app['cpus'], app['mem']]
            app_instances = app['instances']
            app_tasks_running = app['tasksRunning']
            app_deployments = app['deployments']
            running = app_tasks_running > 0
            deploying = len(app_deployments) > 0
            suspended = app_instances == 0 and app_tasks_running == 0
            app_status = 'Deploying' if deploying else 'Running' if running else 'Suspended' if suspended else 'Unknown'
            app_entry.append(app_status)
            app_entry.append(app_instances)
            app_healthy_tasks = app['tasksHealthy']
            app_unhealthy_tasks = app['tasksUnhealthy']
            app_health = 'Unhealthy' if app_unhealthy_tasks > 0 else 'Healthy' if app_healthy_tasks > 0 else 'Unknown'
            app_entry.append(app_health)
            app_table.append(app_entry)
        print(tabulate.tabulate(app_table, headers='firstrow', tablefmt='psql'))
        return len(app_table) - 1
    else:
        if service_name:
            print('No service running with name {} on your ACS cluster'.format(service_name))
        else:
            print('No running services on your ACS cluster')
            return SUCCESS_RETURN_CODE


def realtime_service_list_kubernetes(context, service_name=None, verbose=False):
    label_selector = "type==realtime"
    if service_name is not None:
        label_selector += ",webservicename=={}".format(service_name)

    if verbose:
        print("label selector: {}".format(label_selector))

    try:
        k8s_ops = KubernetesOperations()
        list_result = k8s_ops.get_filtered_deployments(label_selector)
    except ApiException as exc:
        print("Failed to list deployments. {}".format(exc))
        return

    if verbose:
        print("Retrieved deployments: ")
        print(list_result)

    if len(list_result) > 0:
        app_table = [['NAME', 'IMAGE', 'STATUS', 'INSTANCES', 'HEALTH']]
        for app in list_result:
            app_image = app.spec.template.spec.containers[0].image
            app_name = app.metadata.labels['webservicename']
            app_status = app.status.conditions[0].type
            app_instances = app.status.replicas
            app_health = 'Healthy' if app.status.unavailable_replicas is None else 'Unhealthy'
            app_entry = [app_name, app_image, app_status, app_instances, app_health]
            app_table.append(app_entry)
        print(tabulate.tabulate(app_table, headers='firstrow', tablefmt='psql'))
        return len(app_table) - 1
    else:
        if service_name:
            print('No service running with name {} on your ACS cluster'.format(service_name))
        else:
            print('No running services on your ACS cluster')
            return SUCCESS_RETURN_CODE


def realtime_service_run_cluster(context, service_name, input_data, verbose):
    """Run a previously published realtime web service in an ACS cluster."""

    if context.acs_agent_url is None:
        print("")
        print("Please set up your ACS cluster for AML. Run 'az ml env about' for help on setting up your environment.")
        print("")
        return

    headers = {'Content-Type': 'application/json', 'X-Marathon-App-Id': "/{}".format(service_name)}

    if input_data == '':
        sample_url = 'http://' + context.acs_agent_url + ':9091/sample'
        sample_data = get_sample_data(sample_url, headers, verbose)

        if sample_data is None:
            print('No such service {}'.format(service_name))
            return
        elif sample_data == '':
            print(
                "No sample data available. To score with your own data, run: az ml service run realtime -n {} -d <input_data>" #pylint: disable=line-too-long
                .format(service_name))
            return

        input_data = '{{"input":"{}"}}'.format(sample_data)
        print('Using sample data: ' + input_data)

    marathon_url = 'http://' + context.acs_agent_url + ':9091/score'
    result = requests.post(marathon_url, headers=headers, data=input_data, verify=False)
    if verbose:
        print(result.content)

    if result.status_code != 200:
        print('Error scoring the service.')
        print(result.content)
        return

    try:
        result = result.json()
    except ValueError:
        print('Error scoring the service.')
        print(result.content)
        return

    print(result['result'])
    return SUCCESS_RETURN_CODE


def realtime_service_run_kubernetes(context, service_name, input_data, verbose):
    headers = {'Content-Type': 'application/json'}
    try:
        frontend_service_url = get_k8s_frontend_url()
    except ApiException as exc:
        print("Unable to connect to Kubernetes Front-End service. {}".format(exc))
        return
    if input_data is None:
        sample_endpoint = frontend_service_url + service_name + '/sample'
        input_data = get_sample_data(sample_endpoint, headers, verbose)

    scoring_endpoint = frontend_service_url + service_name + '/score'
    result = requests.post(scoring_endpoint, data=input_data, headers=headers)
    if verbose:
        print(result.content)

    if not result.ok:
        print('Error scoring the service.')
        content = result.content.decode()
        if content == "ehostunreach":
            print('Unable to reach the requested host.')
            print('If you just created this service, it may not be available yet. Please try again in a few minutes.')
        elif '%MatchError' in content or 'No such thing' in content:
            print('Unable to find service with name {}.'.format(service_name))
        else:
            print(content)
        return

    try:
        result = result.json()
    except ValueError:
        print('Error scoring the service.')
        print(result.content)
        return

    print(result['result'])
    return SUCCESS_RETURN_CODE


def realtime_service_run(service_name, input_data, verb, context=cli_context):
    _realtime_service_run(service_name, input_data, verb, context)


def _realtime_service_run(service_name, input_data, verb, context=cli_context):
    """
    Execute a previously published realtime web service.
    :param context: CommandLineInterfaceContext object
    :param args: list of str arguments
    """

    verbose = verb

    if verbose:
        print("data: {}".format(input_data))

    if context.in_local_mode():
        return realtime_service_run_local(service_name, input_data, verbose)
    elif context.env_is_k8s:
        return realtime_service_run_kubernetes(context, service_name, input_data, verbose)
    else:
        return realtime_service_run_cluster(context, service_name, input_data, verbose)


