"""
Crawls through the 'source' source and looks for labels starting with 'rancon'.

If such a label is found on a service, then it will register the service in the
'backend'. If the backend supports tag all services will be tagged 'rancon'.
depending on the backend the registration behavior can be influenced by tags
set on the source (e.g. rancon.name, ...).

Every rancon.* tag will be available as variable "%NAME%" in the backend.
Please look through the documentation to make more sense of this, it is easy
but just a little bit complex because of the flexibility.
"""

import asyncio
import sys
import time

from rancon import settings
from rancon import tools
from .version import __version__

import uvloop
import prometheus_client.exposition
import prometheus_client.core
from prometheus_client import Counter, Gauge, Histogram, Summary
import sanic
from sanic import Sanic
from sanic.response import HTTPResponse, text


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = Sanic(__name__)


@app.route("/")
async def index(request):
    """ returns a hello string """
    return text("rancon v{} :)".format(__version__))


@app.route("/metrics")
async def metrics(request):
    """ returns the latest metrics """
    names = request.args.get("name", None)
    registry = prometheus_client.core.REGISTRY
    if names:
        registry = registry.restricted_registry(names)
    tmp = prometheus_client.exposition.generate_latest(registry)
    return HTTPResponse(body_bytes=tmp)


@app.route("/health")
async def health(request):
    """ returns the current health state of the system """
    duration = time.time() - LAST_CALL_ROUTE_SERVICES

    if duration > settings.args.hangup_detection:
        msg = "system hang-up detected, it's been {} seconds since start of "\
              "route_services".format(int(duration))
        raise sanic.exceptions.ServerError(msg)
    return text("OK")


LAST_CALL_ROUTE_SERVICES = time.time()

# NB: documentation does not fit the implementation here. the parameters here should be
# name, labelnames, labelvalues but documented are name, description, so I'm not sure
# what to use here. Also, it's not clear what labelnames and labelvalues should be if they
# were used and how they could be retrieved.
ROUTE_TIME = Summary('rancon_route_services_seconds',
                     'Number of seconds route_services takes')

METRIC_SERVICES_FOUND = Gauge('rancon_discovered_services',
                              'Number of discovered services')

METRIC_SUCCESSFUL_REGS = Counter('rancon_successful_registrations',
                                 'Number of services registered')

METRIC_FAILED_REGS = Counter('rancon_failed_registrations',
                             'Number of failed service registrations')

METRIC_RAISED_REGS = Counter('rancon_registration_exceptions',
                             'Number of exception during service registrations')

METRIC_SUCCESSFUL_DEREGS = Counter('rancon_successful_deregistrations',
                                   'Number of services deregistered, UNUSED')

METRIC_FAILED_DEREGS = Counter('rancon_failed_deregistrations',
                               'Number of failed service deregistrations, '
                               'UNUSED')

METRIC_VERSION = Gauge('rancon_version',
                         'Rancon version number',
                         ('version',)).labels(__version__).set(1)


@ROUTE_TIME.time()
def route_services(schedule_next=5, loop=None):
    """ checks for services to register and then register them with consul """
    if loop is not None:
        loop.call_later(schedule_next, route_services, schedule_next, loop)
    global LAST_CALL_ROUTE_SERVICES
    LAST_CALL_ROUTE_SERVICES = time.time()

    log = tools.getLogger(__name__)
    backend = settings.backend
    source = settings.source

    services_to_route = source.get_services()
    registered_services = []

    METRIC_SERVICES_FOUND.set(len(services_to_route))
    for service in services_to_route:
            try:
                # I think that will re-raise or pass the exception thorug,
                # so we also need to catch it manually
                with METRIC_RAISED_REGS.count_exceptions():
                    success, routed_service = backend.register(service)
                registered_services.append(routed_service)
            except Exception as e:
                success = False
                log.error("EXCEPTION CAUGHT WHILE REGSITERING '{}': {}"
                          .format(str(service), str(e)))
            if success:
                METRIC_SUCCESSFUL_REGS.inc()
            else:
                METRIC_FAILED_REGS.inc()

    if len(registered_services) == 0:
        log.debug("No services registered (of {} services found)"
                  .format(len(services_to_route)))
    backend.cleanup(registered_services)
    log.debug("Run completed @ {}".format(time.ctime()))


def start(sys_argv):
    # prepare
    settings.parse_params(sys_argv)
    # not before here :)
    log = tools.getLogger(__name__)
    # run
    log.error("Start @ {}".format(time.ctime()))

    if not settings.args.continuous:
        route_services()
        sys.exit(0)

    loop = asyncio.get_event_loop()
    loop.call_soon(route_services, settings.args.wait, loop)
    app.run(host="0.0.0.0", port=8000, loop=loop)
    log.info("Exiting.")


def console_entrypoint():
    start(sys.argv[1:])

