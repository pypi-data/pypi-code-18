import os
import sys
import json
from functools import partial
import multiprocessing as mp
import queue
import subprocess
import kubernetes
from kontroller import BaseController, oid
from kontroller import log as _log
from . import client


STATUS = (
    'Creating',
    'Scanning',
    'ScanFinished',
    'Done',
    'Error',
)


def log(*v, **kw):
    _log(*v, **kw)
    sys.stdout.flush()


def imagestream_tags(o):
    return o.status.tags if o.status and o.status.tags else []


def imagestream_tags_by_name(o):
    tags_by_name = {}
    for t in imagestream_tags(o):
        tags_by_name[t.tag] = t
    return tags_by_name


def clairreport_tags_by_name(o):
    tags_by_name = {}
    for t in o.tags:
        tags_by_name[t.tag] = t
    return tags_by_name


def imagestream_tag(o, tag):
    for t in imagestream_tags(o):
        if t.tag == tag:
            return t


def imagestream_tag_docker_image_references(tag):
    return set([ item.docker_image_reference for item in tag.items ])


def imagestream_tags_has_changed(old, new):
    old_tags = imagestream_tags(old)
    new_tags = imagestream_tags(new)

    old_tags_names = set([ t.tag for t in old_tags ])
    if old_tags_names != set([ t.tag for t in new_tags ]):
        return True

    for old_tag in old_tags:
        new_tag = imagestream_tag(new, old_tag.tag)
        old_dirs = imagestream_tag_docker_image_references(old_tag)
        new_dirs = imagestream_tag_docker_image_references(new_tag)
        if old_dirs != new_dirs:
            return True

    return False


class KlairController(BaseController):

    def __init__(self, client, watch, dockercfg=None, *vargs, **kwargs):
        self.client = client
        self.dockercfg = dockercfg

        # caches
        self.crs = {}
        self.iss = {}

        self.pool = mp.Pool(5)
        self.scans = {}

        super(KlairController, self).__init__(watch=watch, *vargs, **kwargs)


    def start(self):
        self.oapi_v1 = self.client.OapiApi()
        self.vapi_v1 = client.VulnerabilityGetupIoV1Api(api_client=self.oapi_v1.api_client)

        self.create_watcher(self.vapi_v1.list_clair_reports)
        self.create_watcher(self.oapi_v1.list_image_stream_for_all_namespaces,
                label_selector='vulnerability.getup.io/clairreport=active')

        self.start_controller(loop_frequency=5)


    def process_objects(self, objs, kind, booting=False):
        log('>>> Processing {} {} objects'.format(len(objs), kind))
        for uid, o in objs.items():
            #log('>>>', oid(o))
            if booting:
                self.added_object(o)
                if o.kind == 'ClairReport' and o.status == 'Scanning':
                    self.start_scanning(o)
            else:
                self.resolve_handler('process', o)


    def added_object(self, o):
        log('++>', oid(o), '@', o.metadata.creation_timestamp)
        self.resolve_handler('added', o)


    def modified_object(self, old, new):
        log('xx>', oid(old), '-->', oid(new), '@', new.metadata.creation_timestamp)
        self.resolve_handler('modified', old, new)


    def deleted_object(self, o):
        log('-->', oid(o), o.metadata.creation_timestamp)
        self.resolve_handler('deleted', o)


    def resolve_handler(self, prefix, o, *vargs, **kwargs):
        handler = getattr(self, '{}_{}'.format(prefix, o.kind.lower()), None)
        if callable(handler):
            return handler(o, *vargs, **kwargs)


    ## ImageStream events
    #####################


    #def process_imagestream(self, o):
    #    pass


    def added_imagestream(self, o):
        k = o.metadata.uid
        self.iss[k] = o
        #self.create_clairreport(o)


    def modified_imagestream(self, old, new):
        if not imagestream_tags_has_changed(old, new):
            return

        log('ImageStream has changed')
        cr = self.find_clairreport(new.metadata.uid)

        if cr:
            self.start_scanning(cr)
        else:
            log('ClairReport not found... creating')
            self.create_clairreport(new)

        for tag in new.status.tags:
            log('   *', tag.tag, tag.items[0].docker_image_reference)
            #for item in tag.items:
            #    log('      ', item.docker_image_reference)


    def deleted_imagestream(self, o):
        k =  o.metadata.uid
        self.iss.pop(k)


    ## ClairReports events
    ######################


    def process_clairreport(self, o):
        log('Processing ClairReport: {} {}'.format(o.metadata.name, o.status))

        if o.status == 'Creating':
            self.start_scanning(o)

        elif o.status == 'ScanFinished':
            scan = self.scans.get(o.metadata.uid)
            if scan is None:
                self.start_scanning(o)
            else:
                self.reconcile_tags(o, scan)


    def added_clairreport(self, o):
        k = o.metadata.uid
        if k in self.crs:
            log('WARN: ClairReport already exists:', o.metadata.name)
        else:
            self.crs[k] = o
            self.process_clairreport(o)


    #def modified_clairreport(self, old, new):
    #    pass


    def deleted_clairreport(self, o):
        try:
            k = o.metadata.uid
            if k in self.crs:
                self.crs.pop(k)
        except KeyError as ex:
            log('WARN: Error deleting ClairReport:', ex)


    def get_clairreport(self, uid):
        return self.crs.get(uid)


    def find_clairreport(self, imageStreamUid):
        for cr in self.crs.values():
            if cr.image_stream_uid == imageStreamUid:
                return cr


    def create_clairreport(self, imageStream):
        tags = [
                client.models.V1ClairReportTag(
                    tag=t.tag,
                    latest_image=t.items[0].image)
                for t in
                imagestream_tags(imageStream) ]

        body = client.models.V1ClairReport(
                api_version='vulnerability.getup.io/v1',
                metadata=kubernetes.client.models.V1ObjectMeta(
                        name=imageStream.metadata.name,
                        namespace=imageStream.metadata.namespace),
                kind='ClairReport',
                status='Creating',
                image_stream_uid=imageStream.metadata.uid,
                image_repository=imageStream.status.docker_image_repository,
                tags=tags)

        log('Creating ClairReport: {m.namespace}/{m.name}'.format(m=body.metadata))

        self.vapi_v1.create_namespaced_clair_report(
                imageStream.metadata.namespace,
                body=body,
                callback=lambda r: log('Created ClairReport: {m.uid} {m.namespace}/{m.name}'.format(m=r.metadata)))


    def update_clairreport_status(self, o, status):
        o.status = status
        o.metadata.resource_version = None

        log('Updating ClairReport status: {m.uid} {m.namespace}/{m.name}.{status}'.format(m=o.metadata, status=status))

        self.vapi_v1.update_namespaced_clair_report(
                namespace=o.metadata.namespace,
                name=o.metadata.name,
                body=o,
                callback=lambda r: log('Updated ClairReport status: {m.uid} {m.namespace}/{m.name}.{status}'.format(m=o.metadata, status=status)))


    def on_scan_finished(self, scan):
        log('Scan finished:', scan)
        o = self.get_clairreport(scan['uid'])
        self.scans[o.metadata.uid] = scan
        self.update_clairreport_status(o, 'ScanFinished')


    def reconcile_tags(self, o, scan):
        log('Reconcile tags: {m.uid} {m.namespace}:{m.name}'.format(m=o.metadata), scan)
        uid, image_repository, reports = scan['uid'], scan['image_repository'], scan['reports']
        updated = False

        for report in reports:
            log('Report:', report)
            rtag, layer_count, vulnerabilities = report['tag'], report['LayerCount'], report['Vulnerabilities']

            for tag in o.tags:
                if tag.tag == rtag:
                    tag.layer_count = layer_count
                    tag.vulnerabilities = [
                            client.models.V1ClairReportVulnerability(
                                name=v['Name'],
                                namespace_name=v.get('NamespaceName', ''),
                                description=v.get('Description', ''),
                                link=v.get('Link', ''),
                                severity=v.get('Severity', ''),
                                fixed_by=v.get('FixedBy', ''))
                            for v in vulnerabilities ]
                    updated = True

        o.status = 'Done'
        self.update_clairreport(o)


    def update_clairreport(self, o):
        o.metadata.resource_version = None

        log('Updating ClairReport: {m.uid} {m.namespace}/{m.name}'.format(m=o.metadata))

        self.vapi_v1.update_namespaced_clair_report(
                namespace=o.metadata.namespace,
                name=o.metadata.name,
                body=o,
                callback=lambda r: log('Updated ClairReport: {m.uid} {m.namespace}/{m.name}'.format(m=o.metadata)))


    def on_scan_error(self, o, result):
        log('Scan error:', type(result), result)

        self.update_clairreport_status(o, 'Error')


    def start_scanning(self, o):
        tags = [ t.tag for t in o.tags ]
        self.pool.apply_async(
            klar,
            args=(o.metadata.uid, o.image_repository, tags, self.dockercfg),
            callback=self.on_scan_finished,
            error_callback=partial(self.on_scan_error, o))

        self.update_clairreport_status(o, 'Scanning')


def klar(uid, image_repository, tags, dockercfg):
    log('Running klar %s' % image_repository)

    try:
        image_server, _ = image_repository.split('/', 1)
        docker_user = dockercfg[image_server]['username']
        docker_password = dockercfg[image_server]['password']
    except KeyError:
        docker_user = os.environ.get('DOCKER_USER')
        docker_password = os.environ.get('DOCKER_PASSWORD')

    klar_bin = os.environ.get('KLAR_BIN', '/klar')
    reports = []

    for tag in tags:
        log('Running klar %s:%s' % (image_repository, tag))
        res = subprocess.run(
                [
                    klar_bin,
                    '%s:%s' % (image_repository, tag)
                ],
                env={
                    'CLAIR_ADDR': os.environ.get('CLAIR_ADDR', 'clairsvc'),
                    'DOCKER_USER': docker_user,
                    'DOCKER_PASSWORD': docker_password,
                    'DOCKER_INSECURE': os.environ.get('DOCKER_INSECURE', 'true'),
                    'REGISTRY_INSECURE': os.environ.get('REGISTRY_INSECURE', 'true'),
                    'JSON_OUTPUT': 'true',
                },
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8')

        try:
            report = json.loads(res.stdout)
        except:
            log('Error decoding json:', res.stderr)
            log('   stdout:', res.stdout)
            log('   stderr:', res.stderr)
            continue

        report.update({'tag': tag})
        reports.append(report)
        log('Running klar %s:%s' % (image_repository, tag))

    scan = {
        'uid': uid,
        'image_repository': image_repository,
        'reports': reports
    }

    return scan
