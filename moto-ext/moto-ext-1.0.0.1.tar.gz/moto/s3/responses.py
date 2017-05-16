from __future__ import unicode_literals

import re

import six
from six.moves.urllib.parse import parse_qs, urlparse

import xmltodict

from moto.core.responses import _TemplateEnvironmentMixin

from moto.s3bucket_path.utils import bucket_name_from_url as bucketpath_bucket_name_from_url, parse_key_name as bucketpath_parse_key_name, is_delete_keys as bucketpath_is_delete_keys


from .exceptions import BucketAlreadyExists, S3ClientError, InvalidPartOrder
from .models import s3_backend, get_canned_acl, FakeGrantee, FakeGrant, FakeAcl, FakeKey
from .utils import bucket_name_from_url, metadata_from_headers
from xml.dom import minidom

REGION_URL_REGEX = r'\.s3-(.+?)\.amazonaws\.com'
DEFAULT_REGION_NAME = 'us-east-1'


def parse_key_name(pth):
    return pth.lstrip("/")


def is_delete_keys(request, path, bucket_name):
    return path == u'/?delete' or (
        path == u'/' and
        getattr(request, "query_string", "") == "delete"
    )


class ResponseObject(_TemplateEnvironmentMixin):

    def __init__(self, backend):
        super(ResponseObject, self).__init__()
        self.backend = backend

    @property
    def should_autoescape(self):
        return True

    def all_buckets(self):
        # No bucket specified. Listing all buckets
        all_buckets = self.backend.get_all_buckets()
        template = self.response_template(S3_ALL_BUCKETS)
        return template.render(buckets=all_buckets)

    def subdomain_based_buckets(self, request):
        host = request.headers.get('host', request.headers.get('Host'))
        if not host:
            host = urlparse(request.url).netloc

        if not host or host.startswith("localhost") or re.match(r"^[^.]+$", host):
            # For localhost or local domain names, default to path-based buckets
            return False

        match = re.match(r'^([^\[\]:]+)(:\d+)?$', host)
        if match:
            match = re.match(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}',
                             match.groups()[0])
            if match:
                return False

        match = re.match(r'^\[(.+)\](:\d+)?$', host)
        if match:
            match = re.match(r'^(((?=.*(::))(?!.*\3.+\3))\3?|[\dA-F]{1,4}:)([\dA-F]{1,4}(\3|:\b)|\2){5}(([\dA-F]{1,4}(\3|:\b|$)|\2){2}|(((2[0-4]|1\d|[1-9])?\d|25[0-5])\.?\b){4})\Z',
                             match.groups()[0], re.IGNORECASE)
            if match:
                return False

        path_based = (host == 's3.amazonaws.com' or re.match(
            r"s3[\.\-]([^.]*)\.amazonaws\.com", host))
        return not path_based

    def is_delete_keys(self, request, path, bucket_name):
        if self.subdomain_based_buckets(request):
            return is_delete_keys(request, path, bucket_name)
        else:
            return bucketpath_is_delete_keys(request, path, bucket_name)

    def parse_bucket_name_from_url(self, request, url):
        if self.subdomain_based_buckets(request):
            return bucket_name_from_url(url)
        else:
            return bucketpath_bucket_name_from_url(url)

    def parse_key_name(self, request, url):
        if self.subdomain_based_buckets(request):
            return parse_key_name(url)
        else:
            return bucketpath_parse_key_name(url)

    def ambiguous_response(self, request, full_url, headers):
        # Depending on which calling format the client is using, we don't know
        # if this is a bucket or key request so we have to check
        if self.subdomain_based_buckets(request):
            return self.key_response(request, full_url, headers)
        else:
            # Using path-based buckets
            return self.bucket_response(request, full_url, headers)

    def bucket_response(self, request, full_url, headers):
        try:
            response = self._bucket_response(request, full_url, headers)
        except S3ClientError as s3error:
            response = s3error.code, {}, s3error.description

        if isinstance(response, six.string_types):
            return 200, {}, response.encode("utf-8")
        else:
            status_code, headers, response_content = response
            return status_code, headers, response_content.encode("utf-8")

    def _bucket_response(self, request, full_url, headers):
        parsed_url = urlparse(full_url)
        querystring = parse_qs(parsed_url.query, keep_blank_values=True)
        method = request.method
        region_name = DEFAULT_REGION_NAME
        region_match = re.search(REGION_URL_REGEX, full_url)
        if region_match:
            region_name = region_match.groups()[0]

        bucket_name = self.parse_bucket_name_from_url(request, full_url)
        if not bucket_name:
            # If no bucket specified, list all buckets
            return self.all_buckets()

        if hasattr(request, 'body'):
            # Boto
            body = request.body
        else:
            # Flask server
            body = request.data
        if body is None:
            body = b''
        if isinstance(body, six.binary_type):
            body = body.decode('utf-8')

        if method == 'HEAD':
            return self._bucket_response_head(bucket_name, headers)
        elif method == 'GET':
            return self._bucket_response_get(bucket_name, querystring, headers)
        elif method == 'PUT':
            return self._bucket_response_put(request, body, region_name, bucket_name, querystring, headers)
        elif method == 'DELETE':
            return self._bucket_response_delete(body, bucket_name, querystring, headers)
        elif method == 'POST':
            return self._bucket_response_post(request, body, bucket_name, headers)
        else:
            raise NotImplementedError(
                "Method {0} has not been impelemented in the S3 backend yet".format(method))

    def _bucket_response_head(self, bucket_name, headers):
        self.backend.get_bucket(bucket_name)
        return 200, {}, ""

    def _bucket_response_get(self, bucket_name, querystring, headers):
        if 'uploads' in querystring:
            for unsup in ('delimiter', 'max-uploads'):
                if unsup in querystring:
                    raise NotImplementedError(
                        "Listing multipart uploads with {} has not been implemented yet.".format(unsup))
            multiparts = list(
                self.backend.get_all_multiparts(bucket_name).values())
            if 'prefix' in querystring:
                prefix = querystring.get('prefix', [None])[0]
                multiparts = [
                    upload for upload in multiparts if upload.key_name.startswith(prefix)]
            template = self.response_template(S3_ALL_MULTIPARTS)
            return template.render(
                bucket_name=bucket_name,
                uploads=multiparts)
        elif 'location' in querystring:
            bucket = self.backend.get_bucket(bucket_name)
            template = self.response_template(S3_BUCKET_LOCATION)
            return template.render(location=bucket.location)
        elif 'lifecycle' in querystring:
            bucket = self.backend.get_bucket(bucket_name)
            if not bucket.rules:
                return 404, {}, "NoSuchLifecycleConfiguration"
            template = self.response_template(
                S3_BUCKET_LIFECYCLE_CONFIGURATION)
            return template.render(rules=bucket.rules)
        elif 'versioning' in querystring:
            versioning = self.backend.get_bucket_versioning(bucket_name)
            template = self.response_template(S3_BUCKET_GET_VERSIONING)
            return template.render(status=versioning)
        elif 'policy' in querystring:
            policy = self.backend.get_bucket_policy(bucket_name)
            if not policy:
                template = self.response_template(S3_NO_POLICY)
                return 404, {}, template.render(bucket_name=bucket_name)
            return 200, {}, policy
        elif 'website' in querystring:
            website_configuration = self.backend.get_bucket_website_configuration(
                bucket_name)
            return website_configuration
        elif 'acl' in querystring:
            bucket = self.backend.get_bucket(bucket_name)
            template = self.response_template(S3_OBJECT_ACL_RESPONSE)
            return template.render(obj=bucket)
        elif 'versions' in querystring:
            delimiter = querystring.get('delimiter', [None])[0]
            encoding_type = querystring.get('encoding-type', [None])[0]
            key_marker = querystring.get('key-marker', [None])[0]
            max_keys = querystring.get('max-keys', [None])[0]
            prefix = querystring.get('prefix', [None])[0]
            version_id_marker = querystring.get('version-id-marker', [None])[0]

            bucket = self.backend.get_bucket(bucket_name)
            versions = self.backend.get_bucket_versions(
                bucket_name,
                delimiter=delimiter,
                encoding_type=encoding_type,
                key_marker=key_marker,
                max_keys=max_keys,
                version_id_marker=version_id_marker
            )
            latest_versions = self.backend.get_bucket_latest_versions(
                bucket_name=bucket_name
            )
            key_list = []
            delete_marker_list = []
            for version in versions:
                if isinstance(version, FakeKey):
                    key_list.append(version)
                else:
                    delete_marker_list.append(version)
            template = self.response_template(S3_BUCKET_GET_VERSIONS)
            return 200, {}, template.render(
                key_list=key_list,
                delete_marker_list=delete_marker_list,
                latest_versions=latest_versions,
                bucket=bucket,
                prefix='',
                max_keys=1000,
                delimiter='',
                is_truncated='false',
            )
        elif querystring.get('list-type', [None])[0] == '2':
            return 200, {}, self._handle_list_objects_v2(bucket_name, querystring)

        bucket = self.backend.get_bucket(bucket_name)
        prefix = querystring.get('prefix', [None])[0]
        if prefix and isinstance(prefix, six.binary_type):
            prefix = prefix.decode("utf-8")
        delimiter = querystring.get('delimiter', [None])[0]
        result_keys, result_folders = self.backend.prefix_query(
            bucket, prefix, delimiter)
        template = self.response_template(S3_BUCKET_GET_RESPONSE)
        return 200, {}, template.render(
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,
            result_keys=result_keys,
            result_folders=result_folders
        )

    def _handle_list_objects_v2(self, bucket_name, querystring):
        template = self.response_template(S3_BUCKET_GET_RESPONSE_V2)
        bucket = self.backend.get_bucket(bucket_name)

        prefix = querystring.get('prefix', [None])[0]
        if prefix and isinstance(prefix, six.binary_type):
            prefix = prefix.decode("utf-8")
        delimiter = querystring.get('delimiter', [None])[0]
        result_keys, result_folders = self.backend.prefix_query(
            bucket, prefix, delimiter)

        fetch_owner = querystring.get('fetch-owner', [False])[0]
        max_keys = int(querystring.get('max-keys', [1000])[0])
        continuation_token = querystring.get('continuation-token', [None])[0]
        start_after = querystring.get('start-after', [None])[0]

        if continuation_token or start_after:
            limit = continuation_token or start_after
            continuation_index = 0
            for key in result_keys:
                if key.name > limit:
                    break
                continuation_index += 1
            result_keys = result_keys[continuation_index:]

        if len(result_keys) > max_keys:
            is_truncated = 'true'
            result_keys = result_keys[:max_keys]
            next_continuation_token = result_keys[-1].name
        else:
            is_truncated = 'false'
            next_continuation_token = None

        return template.render(
            bucket=bucket,
            prefix=prefix or '',
            delimiter=delimiter,
            result_keys=result_keys,
            result_folders=result_folders,
            fetch_owner=fetch_owner,
            max_keys=max_keys,
            is_truncated=is_truncated,
            next_continuation_token=next_continuation_token,
            start_after=None if continuation_token else start_after
        )

    def _bucket_response_put(self, request, body, region_name, bucket_name, querystring, headers):
        if not request.headers.get('Content-Length'):
            return 411, {}, "Content-Length required"
        if 'versioning' in querystring:
            ver = re.search('<Status>([A-Za-z]+)</Status>', body)
            if ver:
                self.backend.set_bucket_versioning(bucket_name, ver.group(1))
                template = self.response_template(S3_BUCKET_VERSIONING)
                return template.render(bucket_versioning_status=ver.group(1))
            else:
                return 404, {}, ""
        elif 'lifecycle' in querystring:
            rules = xmltodict.parse(body)['LifecycleConfiguration']['Rule']
            if not isinstance(rules, list):
                # If there is only one rule, xmldict returns just the item
                rules = [rules]
            self.backend.set_bucket_lifecycle(bucket_name, rules)
            return ""
        elif 'policy' in querystring:
            self.backend.set_bucket_policy(bucket_name, body)
            return 'True'
        elif 'acl' in querystring:
            acl = self._acl_from_headers(request.headers)
            # TODO: Support the XML-based ACL format
            self.backend.set_bucket_acl(bucket_name, acl)
            return ""
        elif 'website' in querystring:
            self.backend.set_bucket_website_configuration(bucket_name, body)
            return ""
        else:
            try:
                new_bucket = self.backend.create_bucket(
                    bucket_name, region_name)
            except BucketAlreadyExists:
                if region_name == DEFAULT_REGION_NAME:
                    # us-east-1 has different behavior
                    new_bucket = self.backend.get_bucket(bucket_name)
                else:
                    raise
            template = self.response_template(S3_BUCKET_CREATE_RESPONSE)
            return 200, {}, template.render(bucket=new_bucket)

    def _bucket_response_delete(self, body, bucket_name, querystring, headers):
        if 'policy' in querystring:
            self.backend.delete_bucket_policy(bucket_name, body)
            return 204, {}, ""
        elif 'lifecycle' in querystring:
            bucket = self.backend.get_bucket(bucket_name)
            bucket.delete_lifecycle()
            return 204, {}, ""

        removed_bucket = self.backend.delete_bucket(bucket_name)

        if removed_bucket:
            # Bucket exists
            template = self.response_template(S3_DELETE_BUCKET_SUCCESS)
            return 204, {}, template.render(bucket=removed_bucket)
        else:
            # Tried to delete a bucket that still has keys
            template = self.response_template(
                S3_DELETE_BUCKET_WITH_ITEMS_ERROR)
            return 409, {}, template.render(bucket=removed_bucket)

    def _bucket_response_post(self, request, body, bucket_name, headers):
        if not request.headers.get('Content-Length'):
            return 411, {}, "Content-Length required"
        path = request.path if hasattr(request, 'path') else request.path_url
        if self.is_delete_keys(request, path, bucket_name):
            return self._bucket_response_delete_keys(request, body, bucket_name, headers)

        # POST to bucket-url should create file from form
        if hasattr(request, 'form'):
            # Not HTTPretty
            form = request.form
        else:
            # HTTPretty, build new form object
            form = {}
            for kv in body.split('&'):
                k, v = kv.split('=')
                form[k] = v

        key = form['key']
        if 'file' in form:
            f = form['file']
        else:
            f = request.files['file'].stream.read()

        new_key = self.backend.set_key(bucket_name, key, f)

        # Metadata
        metadata = metadata_from_headers(form)
        new_key.set_metadata(metadata)

        return 200, {}, ""

    def _bucket_response_delete_keys(self, request, body, bucket_name, headers):
        template = self.response_template(S3_DELETE_KEYS_RESPONSE)

        keys = minidom.parseString(body).getElementsByTagName('Key')
        deleted_names = []
        error_names = []

        for k in keys:
            key_name = k.firstChild.nodeValue
            success = self.backend.delete_key(bucket_name, key_name)
            if success:
                deleted_names.append(key_name)
            else:
                error_names.append(key_name)

        return 200, {}, template.render(deleted=deleted_names, delete_errors=error_names)

    def _handle_range_header(self, request, headers, response_content):
        response_headers = {}
        length = len(response_content)
        last = length - 1
        _, rspec = request.headers.get('range').split('=')
        if ',' in rspec:
            raise NotImplementedError(
                "Multiple range specifiers not supported")

        def toint(i):
            return int(i) if i else None
        begin, end = map(toint, rspec.split('-'))
        if begin is not None:  # byte range
            end = last if end is None else min(end, last)
        elif end is not None:  # suffix byte range
            begin = length - min(end, length)
            end = last
        else:
            return 400, response_headers, ""
        if begin < 0 or end > last or begin > min(end, last):
            return 416, response_headers, ""
        response_headers['content-range'] = "bytes {0}-{1}/{2}".format(
            begin, end, length)
        return 206, response_headers, response_content[begin:end + 1]

    def key_response(self, request, full_url, headers):
        response_headers = {}
        try:
            response = self._key_response(request, full_url, headers)
        except S3ClientError as s3error:
            response = s3error.code, {}, s3error.description

        if isinstance(response, six.string_types):
            status_code = 200
            response_content = response
        else:
            status_code, response_headers, response_content = response

        if status_code == 200 and 'range' in request.headers:
            return self._handle_range_header(request, response_headers, response_content)
        return status_code, response_headers, response_content

    def _key_response(self, request, full_url, headers):
        parsed_url = urlparse(full_url)
        query = parse_qs(parsed_url.query, keep_blank_values=True)
        method = request.method

        key_name = self.parse_key_name(request, parsed_url.path)
        bucket_name = self.parse_bucket_name_from_url(request, full_url)

        if hasattr(request, 'body'):
            # Boto
            body = request.body
            if hasattr(body, 'read'):
                body = body.read()
        else:
            # Flask server
            body = request.data
        if body is None:
            body = b''

        if method == 'GET':
            return self._key_response_get(bucket_name, query, key_name, headers)
        elif method == 'PUT':
            return self._key_response_put(request, body, bucket_name, query, key_name, headers)
        elif method == 'HEAD':
            return self._key_response_head(bucket_name, query, key_name, headers)
        elif method == 'DELETE':
            return self._key_response_delete(bucket_name, query, key_name, headers)
        elif method == 'POST':
            return self._key_response_post(request, body, bucket_name, query, key_name, headers)
        else:
            raise NotImplementedError(
                "Method {0} has not been implemented in the S3 backend yet".format(method))

    def _key_response_get(self, bucket_name, query, key_name, headers):
        response_headers = {}
        if query.get('uploadId'):
            upload_id = query['uploadId'][0]
            parts = self.backend.list_multipart(bucket_name, upload_id)
            template = self.response_template(S3_MULTIPART_LIST_RESPONSE)
            return 200, response_headers, template.render(
                bucket_name=bucket_name,
                key_name=key_name,
                upload_id=upload_id,
                count=len(parts),
                parts=parts
            )
        version_id = query.get('versionId', [None])[0]
        key = self.backend.get_key(
            bucket_name, key_name, version_id=version_id)
        if 'acl' in query:
            template = self.response_template(S3_OBJECT_ACL_RESPONSE)
            return 200, response_headers, template.render(obj=key)

        response_headers.update(key.metadata)
        response_headers.update(key.response_dict)
        return 200, response_headers, key.value

    def _key_response_put(self, request, body, bucket_name, query, key_name, headers):
        response_headers = {}
        if query.get('uploadId') and query.get('partNumber'):
            upload_id = query['uploadId'][0]
            part_number = int(query['partNumber'][0])
            if 'x-amz-copy-source' in request.headers:
                src = request.headers.get("x-amz-copy-source").lstrip("/")
                src_bucket, src_key = src.split("/", 1)
                src_range = request.headers.get(
                    'x-amz-copy-source-range', '').split("bytes=")[-1]

                try:
                    start_byte, end_byte = src_range.split("-")
                    start_byte, end_byte = int(start_byte), int(end_byte)
                except ValueError:
                    start_byte, end_byte = None, None

                key = self.backend.copy_part(
                    bucket_name, upload_id, part_number, src_bucket,
                    src_key, start_byte, end_byte)
                template = self.response_template(S3_MULTIPART_UPLOAD_RESPONSE)
                response = template.render(part=key)
            else:
                key = self.backend.set_part(
                    bucket_name, upload_id, part_number, body)
                response = ""
            response_headers.update(key.response_dict)
            return 200, response_headers, response

        storage_class = request.headers.get('x-amz-storage-class', 'STANDARD')
        acl = self._acl_from_headers(request.headers)

        if 'acl' in query:
            key = self.backend.get_key(bucket_name, key_name)
            # TODO: Support the XML-based ACL format
            key.set_acl(acl)
            return 200, response_headers, ""

        if 'x-amz-copy-source' in request.headers:
            # Copy key
            src_key_parsed = urlparse(request.headers.get("x-amz-copy-source"))
            src_bucket, src_key = src_key_parsed.path.lstrip("/").split("/", 1)
            src_version_id = parse_qs(src_key_parsed.query).get(
                'versionId', [None])[0]
            self.backend.copy_key(src_bucket, src_key, bucket_name, key_name,
                                  storage=storage_class, acl=acl, src_version_id=src_version_id)
            new_key = self.backend.get_key(bucket_name, key_name)
            mdirective = request.headers.get('x-amz-metadata-directive')
            if mdirective is not None and mdirective == 'REPLACE':
                metadata = metadata_from_headers(request.headers)
                new_key.set_metadata(metadata, replace=True)
            template = self.response_template(S3_OBJECT_COPY_RESPONSE)
            response_headers.update(new_key.response_dict)
            return 200, response_headers, template.render(key=new_key)
        streaming_request = hasattr(request, 'streaming') and request.streaming
        closing_connection = headers.get('connection') == 'close'
        if closing_connection and streaming_request:
            # Closing the connection of a streaming request. No more data
            new_key = self.backend.get_key(bucket_name, key_name)
        elif streaming_request:
            # Streaming request, more data
            new_key = self.backend.append_to_key(bucket_name, key_name, body)
        else:
            # Initial data
            new_key = self.backend.set_key(bucket_name, key_name, body,
                                           storage=storage_class)
            request.streaming = True
            metadata = metadata_from_headers(request.headers)
            new_key.set_metadata(metadata)
            new_key.set_acl(acl)
            new_key.website_redirect_location = request.headers.get('x-amz-website-redirect-location')

        template = self.response_template(S3_OBJECT_RESPONSE)
        response_headers.update(new_key.response_dict)
        return 200, response_headers, template.render(key=new_key)

    def _key_response_head(self, bucket_name, query, key_name, headers):
        response_headers = {}
        version_id = query.get('versionId', [None])[0]
        key = self.backend.get_key(
            bucket_name, key_name, version_id=version_id)
        if key:
            response_headers.update(key.metadata)
            response_headers.update(key.response_dict)
            return 200, response_headers, ""
        else:
            return 404, response_headers, ""

    def _acl_from_headers(self, headers):
        canned_acl = headers.get('x-amz-acl', '')
        if canned_acl:
            return get_canned_acl(canned_acl)

        grants = []
        for header, value in headers.items():
            if not header.startswith('x-amz-grant-'):
                continue

            permission = {
                'read': 'READ',
                'write': 'WRITE',
                'read-acp': 'READ_ACP',
                'write-acp': 'WRITE_ACP',
                'full-control': 'FULL_CONTROL',
            }[header[len('x-amz-grant-'):]]

            grantees = []
            for key_and_value in value.split(","):
                key, value = re.match(
                    '([^=]+)="([^"]+)"', key_and_value.strip()).groups()
                if key.lower() == 'id':
                    grantees.append(FakeGrantee(id=value))
                else:
                    grantees.append(FakeGrantee(uri=value))
            grants.append(FakeGrant(grantees, [permission]))

        if grants:
            return FakeAcl(grants)
        else:
            return None

    def _key_response_delete(self, bucket_name, query, key_name, headers):
        if query.get('uploadId'):
            upload_id = query['uploadId'][0]
            self.backend.cancel_multipart(bucket_name, upload_id)
            return 204, {}, ""
        version_id = query.get('versionId', [None])[0]
        self.backend.delete_key(bucket_name, key_name, version_id=version_id)
        template = self.response_template(S3_DELETE_OBJECT_SUCCESS)
        return 204, {}, template.render()

    def _complete_multipart_body(self, body):
        ps = minidom.parseString(body).getElementsByTagName('Part')
        prev = 0
        for p in ps:
            pn = int(p.getElementsByTagName(
                'PartNumber')[0].firstChild.wholeText)
            if pn <= prev:
                raise InvalidPartOrder()
            yield (pn, p.getElementsByTagName('ETag')[0].firstChild.wholeText)

    def _key_response_post(self, request, body, bucket_name, query, key_name, headers):
        if body == b'' and 'uploads' in query:
            metadata = metadata_from_headers(request.headers)
            multipart = self.backend.initiate_multipart(
                bucket_name, key_name, metadata)

            template = self.response_template(S3_MULTIPART_INITIATE_RESPONSE)
            response = template.render(
                bucket_name=bucket_name,
                key_name=key_name,
                upload_id=multipart.id,
            )
            return 200, {}, response

        if query.get('uploadId'):
            body = self._complete_multipart_body(body)
            upload_id = query['uploadId'][0]
            key = self.backend.complete_multipart(bucket_name, upload_id, body)
            template = self.response_template(S3_MULTIPART_COMPLETE_RESPONSE)
            return template.render(
                bucket_name=bucket_name,
                key_name=key.name,
                etag=key.etag,
            )
        elif 'restore' in query:
            es = minidom.parseString(body).getElementsByTagName('Days')
            days = es[0].childNodes[0].wholeText
            key = self.backend.get_key(bucket_name, key_name)
            r = 202
            if key.expiry_date is not None:
                r = 200
            key.restore(int(days))
            return r, {}, ""
        else:
            raise NotImplementedError(
                "Method POST had only been implemented for multipart uploads and restore operations, so far")


S3ResponseInstance = ResponseObject(s3_backend)

S3_ALL_BUCKETS = """<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01">
  <Owner>
    <ID>bcaf1ffd86f41161ca5fb16fd081034f</ID>
    <DisplayName>webfile</DisplayName>
  </Owner>
  <Buckets>
    {% for bucket in buckets %}
      <Bucket>
        <Name>{{ bucket.name }}</Name>
        <CreationDate>2006-02-03T16:45:09.000Z</CreationDate>
      </Bucket>
    {% endfor %}
 </Buckets>
</ListAllMyBucketsResult>"""

S3_BUCKET_GET_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>{{ bucket.name }}</Name>
  <Prefix>{{ prefix }}</Prefix>
  <MaxKeys>1000</MaxKeys>
  <Delimiter>{{ delimiter }}</Delimiter>
  <IsTruncated>false</IsTruncated>
  {% for key in result_keys %}
    <Contents>
      <Key>{{ key.name }}</Key>
      <LastModified>{{ key.last_modified_ISO8601 }}</LastModified>
      <ETag>{{ key.etag }}</ETag>
      <Size>{{ key.size }}</Size>
      <StorageClass>{{ key.storage_class }}</StorageClass>
      <Owner>
        <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
        <DisplayName>webfile</DisplayName>
      </Owner>
    </Contents>
  {% endfor %}
  {% if delimiter %}
    {% for folder in result_folders %}
      <CommonPrefixes>
        <Prefix>{{ folder }}</Prefix>
      </CommonPrefixes>
    {% endfor %}
  {% endif %}
  </ListBucketResult>"""

S3_BUCKET_GET_RESPONSE_V2 = """<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>{{ bucket.name }}</Name>
  <Prefix>{{ prefix }}</Prefix>
  <MaxKeys>{{ max_keys }}</MaxKeys>
  <KeyCount>{{ result_keys | length }}</KeyCount>
{% if delimiter %}
  <Delimiter>{{ delimiter }}</Delimiter>
{% endif %}
  <IsTruncated>{{ is_truncated }}</IsTruncated>
{% if next_continuation_token %}
  <NextContinuationToken>{{ next_continuation_token }}</NextContinuationToken>
{% endif %}
{% if start_after %}
  <StartAfter>{{ start_after }}</StartAfter>
{% endif %}
  {% for key in result_keys %}
    <Contents>
      <Key>{{ key.name }}</Key>
      <LastModified>{{ key.last_modified_ISO8601 }}</LastModified>
      <ETag>{{ key.etag }}</ETag>
      <Size>{{ key.size }}</Size>
      <StorageClass>{{ key.storage_class }}</StorageClass>
      {% if fetch_owner %}
      <Owner>
        <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
        <DisplayName>webfile</DisplayName>
      </Owner>
      {% endif %}
    </Contents>
  {% endfor %}
  {% if delimiter %}
    {% for folder in result_folders %}
      <CommonPrefixes>
        <Prefix>{{ folder }}</Prefix>
      </CommonPrefixes>
    {% endfor %}
  {% endif %}
  </ListBucketResult>"""

S3_BUCKET_CREATE_RESPONSE = """<CreateBucketResponse xmlns="http://s3.amazonaws.com/doc/2006-03-01">
  <CreateBucketResponse>
    <Bucket>{{ bucket.name }}</Bucket>
  </CreateBucketResponse>
</CreateBucketResponse>"""

S3_DELETE_BUCKET_SUCCESS = """<DeleteBucketResponse xmlns="http://s3.amazonaws.com/doc/2006-03-01">
  <DeleteBucketResponse>
    <Code>204</Code>
    <Description>No Content</Description>
  </DeleteBucketResponse>
</DeleteBucketResponse>"""

S3_DELETE_BUCKET_WITH_ITEMS_ERROR = """<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>BucketNotEmpty</Code>
<Message>The bucket you tried to delete is not empty</Message>
<BucketName>{{ bucket.name }}</BucketName>
<RequestId>asdfasdfsdafds</RequestId>
<HostId>sdfgdsfgdsfgdfsdsfgdfs</HostId>
</Error>"""

S3_BUCKET_LOCATION = """<?xml version="1.0" encoding="UTF-8"?>
<LocationConstraint xmlns="http://s3.amazonaws.com/doc/2006-03-01/">{{ location }}</LocationConstraint>"""

S3_BUCKET_LIFECYCLE_CONFIGURATION = """<?xml version="1.0" encoding="UTF-8"?>
<LifecycleConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    {% for rule in rules %}
    <Rule>
        <ID>{{ rule.id }}</ID>
        <Prefix>{{ rule.prefix if rule.prefix != None }}</Prefix>
        <Status>{{ rule.status }}</Status>
        {% if rule.storage_class %}
        <Transition>
            {% if rule.transition_days %}
               <Days>{{ rule.transition_days }}</Days>
            {% endif %}
            {% if rule.transition_date %}
               <Date>{{ rule.transition_date }}</Date>
            {% endif %}
           <StorageClass>{{ rule.storage_class }}</StorageClass>
        </Transition>
        {% endif %}
        {% if rule.expiration_days or rule.expiration_date %}
        <Expiration>
            {% if rule.expiration_days %}
               <Days>{{ rule.expiration_days }}</Days>
            {% endif %}
            {% if rule.expiration_date %}
               <Date>{{ rule.expiration_date }}</Date>
            {% endif %}
        </Expiration>
        {% endif %}
    </Rule>
    {% endfor %}
</LifecycleConfiguration>
"""

S3_BUCKET_VERSIONING = """<?xml version="1.0" encoding="UTF-8"?>
<VersioningConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Status>{{ bucket_versioning_status }}</Status>
</VersioningConfiguration>
"""

S3_BUCKET_GET_VERSIONING = """<?xml version="1.0" encoding="UTF-8"?>
{% if status is none %}
    <VersioningConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"/>
{% else %}
    <VersioningConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Status>{{ status }}</Status>
    </VersioningConfiguration>
{% endif %}
"""

S3_BUCKET_GET_VERSIONS = """<?xml version="1.0" encoding="UTF-8"?>
<ListVersionsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01">
    <Name>{{ bucket.name }}</Name>
    <Prefix>{{ prefix }}</Prefix>
    <KeyMarker>{{ key_marker }}</KeyMarker>
    <MaxKeys>{{ max_keys }}</MaxKeys>
    <IsTruncated>{{ is_truncated }}</IsTruncated>
    {% for key in key_list %}
    <Version>
        <Key>{{ key.name }}</Key>
        <VersionId>{{ key.version_id }}</VersionId>
        <IsLatest>{% if latest_versions[key.name] == key.version_id %}true{% else %}false{% endif %}</IsLatest>
        <LastModified>{{ key.last_modified_ISO8601 }}</LastModified>
        <ETag>{{ key.etag }}</ETag>
        <Size>{{ key.size }}</Size>
        <StorageClass>{{ key.storage_class }}</StorageClass>
        <Owner>
            <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
            <DisplayName>webfile</DisplayName>
        </Owner>
    </Version>
    {% endfor %}
    {% for marker in delete_marker_list %}
    <DeleteMarker>
        <Key>{{ marker.key.name }}</Key>
        <VersionId>{{ marker.version_id }}</VersionId>
        <IsLatest>{% if latest_versions[marker.key.name] == marker.version_id %}true{% else %}false{% endif %}</IsLatest>
        <LastModified>{{ marker.key.last_modified_ISO8601 }}</LastModified>
        <Owner>
            <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
            <DisplayName>webfile</DisplayName>
        </Owner>
    </DeleteMarker>
    {% endfor %}
</ListVersionsResult>
"""

S3_DELETE_KEYS_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<DeleteResult xmlns="http://s3.amazonaws.com/doc/2006-03-01">
{% for k in deleted %}
<Deleted>
<Key>{{k}}</Key>
</Deleted>
{% endfor %}
{% for k in delete_errors %}
<Error>
<Key>{{k}}</Key>
</Error>
{% endfor %}
</DeleteResult>"""

S3_DELETE_OBJECT_SUCCESS = """<DeleteObjectResponse xmlns="http://s3.amazonaws.com/doc/2006-03-01">
  <DeleteObjectResponse>
    <Code>200</Code>
    <Description>OK</Description>
  </DeleteObjectResponse>
</DeleteObjectResponse>"""

S3_OBJECT_RESPONSE = """<PutObjectResponse xmlns="http://s3.amazonaws.com/doc/2006-03-01">
      <PutObjectResponse>
        <ETag>{{ key.etag }}</ETag>
        <LastModified>{{ key.last_modified_ISO8601 }}</LastModified>
      </PutObjectResponse>
    </PutObjectResponse>"""

S3_OBJECT_ACL_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
    <AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
      <Owner>
        <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
        <DisplayName>webfile</DisplayName>
      </Owner>
      <AccessControlList>
        {% for grant in obj.acl.grants %}
        <Grant>
          {% for grantee in grant.grantees %}
          <Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:type="{{ grantee.type }}">
            {% if grantee.uri %}
            <URI>{{ grantee.uri }}</URI>
            {% endif %}
            {% if grantee.id %}
            <ID>{{ grantee.id }}</ID>
            {% endif %}
            {% if grantee.display_name %}
            <DisplayName>{{ grantee.display_name }}</DisplayName>
            {% endif %}
          </Grantee>
          {% endfor %}
          {% for permission in grant.permissions %}
          <Permission>{{ permission }}</Permission>
          {% endfor %}
        </Grant>
        {% endfor %}
      </AccessControlList>
    </AccessControlPolicy>"""

S3_OBJECT_COPY_RESPONSE = """\
<CopyObjectResult xmlns="http://doc.s3.amazonaws.com/2006-03-01">
    <ETag>{{ key.etag }}</ETag>
    <LastModified>{{ key.last_modified_ISO8601 }}</LastModified>
</CopyObjectResult>"""

S3_MULTIPART_INITIATE_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<InitiateMultipartUploadResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Bucket>{{ bucket_name }}</Bucket>
  <Key>{{ key_name }}</Key>
  <UploadId>{{ upload_id }}</UploadId>
</InitiateMultipartUploadResult>"""

S3_MULTIPART_UPLOAD_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<CopyPartResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <LastModified>{{ part.last_modified_ISO8601 }}</LastModified>
  <ETag>{{ part.etag }}</ETag>
</CopyPartResult>"""

S3_MULTIPART_LIST_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<ListPartsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Bucket>{{ bucket_name }}</Bucket>
  <Key>{{ key_name }}</Key>
  <UploadId>{{ upload_id }}</UploadId>
  <StorageClass>STANDARD</StorageClass>
  <Initiator>
    <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
    <DisplayName>webfile</DisplayName>
  </Initiator>
  <Owner>
    <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
    <DisplayName>webfile</DisplayName>
  </Owner>
  <StorageClass>STANDARD</StorageClass>
  <PartNumberMarker>1</PartNumberMarker>
  <NextPartNumberMarker>{{ count }} </NextPartNumberMarker>
  <MaxParts>{{ count }}</MaxParts>
  <IsTruncated>false</IsTruncated>
  {% for part in parts %}
  <Part>
    <PartNumber>{{ part.name }}</PartNumber>
    <LastModified>{{ part.last_modified_ISO8601 }}</LastModified>
    <ETag>{{ part.etag }}</ETag>
    <Size>{{ part.size }}</Size>
  </Part>
  {% endfor %}
</ListPartsResult>"""

S3_MULTIPART_COMPLETE_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<CompleteMultipartUploadResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Location>http://{{ bucket_name }}.s3.amazonaws.com/{{ key_name }}</Location>
  <Bucket>{{ bucket_name }}</Bucket>
  <Key>{{ key_name }}</Key>
  <ETag>{{ etag }}</ETag>
</CompleteMultipartUploadResult>
"""

S3_ALL_MULTIPARTS = """<?xml version="1.0" encoding="UTF-8"?>
<ListMultipartUploadsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Bucket>{{ bucket_name }}</Bucket>
  <KeyMarker></KeyMarker>
  <UploadIdMarker></UploadIdMarker>
  <MaxUploads>1000</MaxUploads>
  <IsTruncated>False</IsTruncated>
  {% for upload in uploads %}
  <Upload>
    <Key>{{ upload.key_name }}</Key>
    <UploadId>{{ upload.id }}</UploadId>
    <Initiator>
      <ID>arn:aws:iam::123456789012:user/user1-11111a31-17b5-4fb7-9df5-b111111f13de</ID>
      <DisplayName>user1-11111a31-17b5-4fb7-9df5-b111111f13de</DisplayName>
    </Initiator>
    <Owner>
      <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
      <DisplayName>webfile</DisplayName>
    </Owner>
    <StorageClass>STANDARD</StorageClass>
    <Initiated>2010-11-10T20:48:33.000Z</Initiated>
  </Upload>
  {% endfor %}
</ListMultipartUploadsResult>
"""

S3_NO_POLICY = """<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>NoSuchBucketPolicy</Code>
  <Message>The bucket policy does not exist</Message>
  <BucketName>{{ bucket_name }}</BucketName>
  <RequestId>0D68A23BB2E2215B</RequestId>
  <HostId>9Gjjt1m+cjU4OPvX9O9/8RuvnG41MRb/18Oux2o5H5MY7ISNTlXN+Dz9IG62/ILVxhAGI0qyPfg=</HostId>
</Error>
"""
