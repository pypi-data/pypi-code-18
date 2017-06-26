"""
Takes input json and massages it to make sconbld json (test edit)
"""
from __future__ import print_function

import sys
import sys
import os
import json
import re
import datetime
from pyTableFormat import TableFormat, Table_Formattable_Object

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
# apparently python datetime is stupid and doesn't support zulu
# http://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-dont-include-z-zulu-or-zero-offset

class Property(object):
    '''
    Slightly more advanced property value that can do special handling of
    representation for dict or datetime types. 
    Valid values for prop_type = 
    'S' ( for string )
    'D' ( for dict )
    'T' ( for datetime )
    '''
    def __init__(self, prop_name, prop_value, prop_type=None):
        self.prop_name = prop_name
        self.prop_value = prop_value
        self.key_type = ''
        if prop_type is None:
            prop_type = 'S' # string
        elif prop_type == 'T':
            self.dto = self.process_datetime(prop_value)
            self.prop_value = prop_value
        else:
            self.prop_type = prop_type

    def get(self, search):
        try:
            if self.prop_type == 'D':
                return self.prop_value.get(search)
        except:
            return self.__repr__()
    def __repr__(self):
        if 'dict' in str(type(self.prop_value)):
            str_dict = str(self.prop_value)
            return u''.join((str_dict)).encode('utf-8').strip()
        try:
            if self.prop_value is None:
                self.prop_value = ''
            return u''.join((self.prop_value)).encode('utf-8').strip()
        except Exception as e:
            msg = ("Exception: %s, trying to unicode encode: %s" % (str(e), str(self.prop_value)))
            print(msg, file=sys.stderr)
            return str(self.prop_value)
    def process_datetime(self, dstring):
        try:
            dto = datetime.datetime.strptime(dstring, DATETIME_FORMAT)
        except:
            dto = 'ERROR'
        return dto


class Entry(Table_Formattable_Object):
    """
    Holds entries coming back from the API json and
    supporting methods to generate print
    """
    def __init__(self, **kwargs):
        self.virtualization_type = Property('virtualization_type',
                                            kwargs.get('virtualization_type'))
        self.vpc_id = Property('vpc_id', kwargs.get('vpc_id'))
        self.name = Property('name', kwargs.get('name'))

        self.instance_id = Property('instance_id', kwargs.get('instance_id'))

        self.alias = Property('alias', kwargs.get('alias'))
        self.subnet_id = Property('subnet_id', kwargs.get('subnet_id'))
        self.private_ip = Property('private_ip', kwargs.get('private_ip'))
        self.account_id = Property('account_id', kwargs.get('account_id'))
        self.tags = Property('tags', kwargs.get('tags'), prop_type='D')
        self.state = Property('state', kwargs.get('state'))
        self.image_id = Property('image_id', kwargs.get('image_id'))
        self.instance_type = Property('instance_type', kwargs.get('instance_type'))
        self.public_dns_name = Property('public_dns_name', kwargs.get('public_dns_name'))
        self.key_name = Property('key_name', kwargs.get('key_name'))
        self.launch_time = Property('launch_time', kwargs.get('launch_time'), prop_type='T')
        try:
            self.uai = Property('uai', self.tags.get('UAI'))
        except:
            pass
        self.dict_extend_values = {'private_ip': 16,
                                   'alias': 20,
                                   'tags': 20,
                                   'vpc_id': 15,
                                   'name': 30,
                                   'subnet_id': 25,
                                   'virtualization_type': 25,
                                   'state': 15,
                                   'account_id': 14,
                                   'image_id': 15,
                                   'instance_type': 12,
                                   'instance_id': 15,
                                   'public_dns_name': 30,
                                   'uai': 15,
                                   'launch_time': 22}
    def dumpself(self):
        return "Name: '%s'" % self.name
    def dumpdict(self):
        return_dict = {}
        for attr in dir(self):
            if (
                    '__' not in attr and
                    'instancemethod' not in str(type(getattr(self, attr))) and
                    'dict' not in str(type(getattr(self, attr))) and
                    'dump_ignore_attrs' not in attr):
                return_dict[attr] = str(getattr(self, attr))
        return return_dict
    def return_props(self):
        """
        returns just the list of properties of type Property()
        """
        attrs = [x for x in dir(self) if 'Property' in str(type(getattr(self, x)))]
        return attrs
    def dictify(self):
        dict_attrs = {}
        for attr in self.return_props():
            dict_attrs[attr] = getattr(self, attr).prop_value
        return dict_attrs
    def in_me(self, prop_name, prop_value_regex_obj):

        if prop_name == 'tag_key':
            tag_dict = getattr(self, 'tags').prop_value
            for key, value in tag_dict.iteritems():
                try:
                    match = re.search(prop_value_regex_obj,
                                      str(key).encode('utf-8'))
                except UnicodeEncodeError:
                    pass
                if match:
                    return True
            return False

        elif prop_name == 'tag_value':
            tag_dict = getattr(self, 'tags').prop_value
            for key, value in tag_dict.iteritems():
                try:
                    match = re.search(prop_value_regex_obj,
                                      str(value).encode('utf-8'))
                except UnicodeEncodeError:
                    pass
                if match:
                    return True
            return False
        # if prop_name in self.tags.prop_value:
        #     match = re.search(prop_value_regex_obj, self.tags.get(prop_name))
        #     if match:
        #         return True
        elif prop_name in self.return_props():
            match = False
            try:
                match = re.search(prop_value_regex_obj,
                                  str(getattr(self, prop_name).prop_value).encode('utf-8'))
            except Exception as e:
                log_msg = ("Exception '%s'. Failure with regex search match on entry: '%s'" %
                           (str(e), str(self.dumpdict())))
                print(log_msg, file=sys.stderr)
            if match:
                return True
    def is_within_datetime_range(self, dto_low, dto_high):
        ''' Takes datetime objects and returns true if entry.launch_time
        is within range
        '''
        # print("LAUNCH TIME IS: %s" % str(self.launch_time.dto))
        if self.launch_time.dto > dto_low and self.launch_time.dto < dto_high:
            return True
        else:
            return False
    def __eq__(self, other):
        return self.instance_id.prop_value == other.instance_id.prop_value
    def __hash__(self):
        return hash(('instance_id', self.instance_id.prop_value))

class NodeSet(object):
    def __init__(self, fname):
        self.entries = self.load(fname) # list of Entry objects
        self.vpcs_unique = self.find_unique_vpcs()
        self.date_range_low = datetime.datetime.now() # set to dto now for now
        self.date_range_high = datetime.datetime.now()
        self.date_range_string = self.build_dtos_default()
    def dictify_entries(self):
        attrs = []
        for entry in self.entries:
            attrs.append(entry.dictify())
        return attrs
    def vpc_stats(self):
        msg = ''
        vpc_counts = [{'vpc_id':'', 'instance_count':0}]
        for vpc in self.vpcs_unique:
            vpc_entries = [x for x in self.entries if x.vpc_id.prop_value == vpc]
            vcount = {'vpc_id': vpc, 'instance_count': len(vpc_entries)}
            vpc_counts.append(vcount)
        fmt = "VPC ID: {0:40}{1:5}"
        from operator import itemgetter
        sorted_vpc_counts = sorted(vpc_counts, key=itemgetter('instance_count'))
        for vpc_count in sorted_vpc_counts:
            msg += ("%s" % fmt.format(vpc_count.get('vpc_id'),
                                      vpc_count.get('instance_count')))

    def find_tag_in_vpc(self, vpc_id, tag_name, tag_value_regex):
        """
        Searches for a tag name/value within a given vpc ID
        and returns a list of the instance IDs
        """
        results = []
        try:
            rtv = re.compile(tag_value_regex, re.IGNORECASE)
        except:
            return [{'ERR - regex compile'}]
        vpc_entries = [x for x in self.entries if x.vpc_id.prop_value == vpc_id]
        for entry in vpc_entries:
            if tag_name in entry.tags.prop_value:
                match = re.search(rtv, entry.tags.prop_value.get(tag_name))
                if match:
                    results.append(entry)
        return results
    def find_tag(self, tag_name, tag_value_regex):
        results = []
        log_msg = "Tag name is '%s' and regex is '%s'" % (str(tag_name), str(tag_value_regex))
        print(log_msg, sys.stderr)
        try:
            rtv = re.compile(tag_value_regex, re.IGNORECASE)
        except Exception as e:
            log_msg = ("HRMMMMM: %s" % str(e))
            print(log_msg, file=sys.stderr)
            return [{'ERR - regex compile'}]
        for i, entry in enumerate(self.entries):
            if entry.in_me(tag_name, rtv):
                results.append(entry)
        return results
    def find_unique_vpcs(self):
        vpcs = [x.vpc_id.prop_value for x in self.entries]
        vpcs_unique = list(set(vpcs))
        return vpcs_unique
    def find_missing_vpcids(self):
        return len([x for x in self.entries if x.vpc_id == ''])
    def find_missing_name_tags(self):
        results = []
        for entry in self.entries:
            if 'Name' in entry.tags.prop_value:
                if entry.tags.prop_value.get('Name') == '':
                    results.append(entry)
        print("NUMBER OF MISSING RESULTS: %d" % len(results))
        return results
    def dumpstats(self, html=None):
        if html is None:
            html = True
        msg = ''
        msg += "-----------------------------\n"
        msg += 'Number of entries: %s\n' % str(len(self.entries))
        msg += 'Number of unique vpcs: %s\n' % str(len(self.vpcs_unique))
        msg += "Number of entries with blank vpc_id: %s\n" % str(self.find_missing_vpcids())
        msg += ("Number of entries with blank/missing " +
                "'Name' tags: %s\n" % str(len(self.find_missing_name_tags())))
        msg += "-----------------------------\n"
        if html:
            msg = msg.replace('\n','<br>')
        return msg
    def load(self, fname):
        with open(fname) as f:
            j = json.load(f)
            nodes = []
            for key in j:
                props = {}
                props['virtualization_type'] = key.get('VirtualizationType')
                props['vpc_id'] = key.get('VpcId')
                props['name'] = key.get('Name')
                props['instance_id'] = key.get('InstanceId')
                props['alias'] = key.get('Alias')
                props['subnet_id'] = key.get('SubnetId')
                props['private_ip'] = key.get('PrivateIpAddress')
                props['account_id'] = key.get('AccountId')
                props['image_id'] = key.get('ImageId')
                props['instance_type'] = key.get('InstanceType')
                props['public_dns_name'] = key.get('PublicDnsName')
                props['key_name'] = key.get('KeyName')
                props['launch_time'] = key.get('LaunchTime')
                tags = {}
                props['state'] = ''
                try:
                    for tag in key['Tags']:
                        tags[tag.get('Key')] = tag.get('Value')
                except:
                    pass
                try:
                    for tag, val in key['State'].iteritems():
                        if tag == 'Name':
                            props['state'] = val
                except:
                    pass
                props['tags'] = tags
                entry = Entry(**props)
                nodes.append(entry)
        return nodes
    def match_nats_to_vpc_ids(self, html=None):
        counts = 0
        if html is None:
            html = True
        msg = ''
        for vpcid in self.vpcs_unique:
            nats_results = self.find_tag_in_vpc(vpcid, 'Name', '.*-NAT')
            bass_results = self.find_tag_in_vpc(vpcid, 'Name', '.*bastion.*')
            if len(nats_results) > 0:
                counts += 1
            if len(nats_results) > 0 and len(bass_results) > 1:
                msg += ('########### BASTIONS for VPC ID %s\n' % str(vpcid))
                for bas in bass_results:
                    msg += ('# %s\n' % bas.name.prop_value)
                    msg += ('[BASTION-%s]\n' % bas.private_ip.prop_value)
                    msg += ('%s\n\n' % bas.private_ip.prop_value)
                msg += ('########### NATS for VPC ID %s\n' % str(vpcid))
                for nat in nats_results:
                    msg += ('# %s\n' % nat.name.prop_value)
                    msg += ('[NAT-%s]\n' % nat.private_ip.prop_value)
                    msg += ('%s\n\n' % nat.private_ip.prop_value)
                msg += '# ==================================================================\n'
        msg += "VPCs with NATs: %s / %s\n" % (str(counts), str(len(self.vpcs_unique)))
        if html:
            msg = msg.replace('\n', '<br>')
        return msg
    def format_results(self, results, html=None):
        msg = "{0:40}{1:10}".format("Number of Results:", str(len(results)))
        msg += '<table border=1>'
        if html is None:
            html_bool = True
        else:
            html_bool = False
        if len(results) > 0:
            if html_bool:
                try:
                    msg += '<tr>'
                    msg += (results[0].dumpself_tableformat_header(html=html_bool))
                    msg += '</tr>'
                    for entry in results:
                        msg += '<tr>'
                        msg += entry.dumpself_tableformat(html=html_bool)
                        msg += '</tr>'
                    msg += '</table>'
                    return msg
                except Exception as e:
                    log_msg = "Error in results formatting: " + str(e)
                    print(log_msg, file=sys.stderr)
                    msg += str(e)
            else:
                msg += (results[0].dumpself_tableformat_header(html=html_bool))
                for entry in results:
                        msg += entry.dumpself_tableformat(html=html_bool)
                return msg
        else:
            msg += "EMPTY RESULTS"
            return msg
    def within_date_range(self, results):
        '''
        returns list that matches the datetime ranges
        '''
        return [x for x in results if x.is_within_datetime_range(self.date_range_low, self.date_range_high)]
    def build_dtos(self, date_range_string=None):
        '''
        Builds from self.date_range_string and builds the datetime objects
        for self.date_range_low and date_range_high
        date_range is a string in the format "YYYYMMDD-YYYYMMDD"
        '''
        if date_range_string is None:
            self.date_range_string = self.build_dtos_default()
        else:
            self.date_range_string = date_range_string
        lowstring = self.date_range_string.split('-')[0]
        highstring = self.date_range_string.split('-')[1]
        self.date_range_high = datetime.datetime.strptime(highstring, '%Y%m%d')
        self.date_range_low = datetime.datetime.strptime(lowstring, '%Y%m%d')
        print("DATE RANGE HIGH OBJ: '%s'" % str(self.date_range_high))
        print("DATE RANGE LOW OBJ: '%s'" % str(self.date_range_low))
    def build_dtos_default(self):
        now = datetime.datetime.now()
        nowstring = datetime.datetime.strftime(now, '%Y%m%d')
        date_range = '19700101-' + nowstring
        print("SETTING DATE RANGE DEFAULT: '%s' " % date_range)
        return date_range
    def search_tag(self, search_tags_dict, gimmestring=None, date_range=None):
        '''
        Search for a given set of tags in the inventory. Takes a dictionary of
        tags as keys with values of regex to search.
        gimmestring is a boolean and will return string results instead of list
        when set to True.
        date_range is a string in the format "YYYYMMDD-YYYYMMDD"
        date_range defaults to "19700101-(now)" if none is specified
        '''
        if gimmestring is None:
            gimmestring = True
        try:
            self.build_dtos(date_range_string=date_range)
        except Exception as ex:
            print("using default date range due to Exception parsing date_range: %s" % str(ex))
            self.build_dtos()
        final_results = []
        results = []
        match_policy = 'AND'
        print("match policy = " + str(match_policy), sys.stderr)
        if match_policy.upper() == 'OR':
            for key, val in search_tags_dict.iteritems():
                subsearch = self.find_tag(key, val)
                for item in subsearch:
                    results.append(item)
            final_results = results
        else:
            subsearches = []
            allresults = []
            subresults = []
            for key, val in search_tags_dict.iteritems():
                subsearch = self.find_tag(key, val)
                subsearches.append(subsearch)
                for item in subsearch:
                    allresults.append(item)
            # sort by length first to make faster
            subsearches.sort(key=lambda x: len(x))
            log_msg = ("NUMBER OF SUBSEARCHES: %d\n" % len(subsearches))
            log_msg += ("NUMBER OF ENTRIES IN ALLRESULTS: %d" % len(allresults))
            print(log_msg, file=sys.stderr)
            for item in allresults:
                not_found = False
                for subsearch in subsearches:
                    if item not in subsearch:
                        not_found = True
                        break
                if not_found != True:
                    subresults.append(item)
            subresults = list(set(subresults))
            # give objects instead of strings
            final_results = subresults
        # now finally filter out based on date range
        print("RESULTS BEFORE DATE FILTER: '%d'" % len(final_results))
        final_results = self.within_date_range(final_results)
        print("RESULTS AFTER DATE FILTER: '%d'" % len(final_results))
        if gimmestring:
            return self.format_results(final_results)
        else:
            return final_results
    def gen_csv_string(self, results):
        msg = ''
        if len(results) > 0:
            msg += results[0].dumpself_csv_header()
            for result in results:
                msg += result.dumpself_csv()
        return msg

def debug():
    d = {'name': 'proxy'}
    r = nodeset.search_tag(d, gimmestring=False, date_range='19701001-20161001')
    print(nodeset.format_results(r, html=False))

if __name__ == '__main__':
    nodeset = NodeSet('lib/output.json')
    debug()
