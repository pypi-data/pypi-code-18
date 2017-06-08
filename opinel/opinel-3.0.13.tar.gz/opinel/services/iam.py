# -*- coding: utf-8 -*-

import re

from opinel.utils.aws import handle_truncated_response
from opinel.utils.console import printInfo, printError, printException



def add_user_to_group(iam_client, user, group, user_info = None, dry_run = False, quiet = False):
    """
    Add an IAM user to an IAM group and updates the user info if needed

    :param iam_client:
    :param group:
    :param user:
    :param user_info:
    :param dry_run:
    :return:
    """
    if not dry_run:
        printInfo('Adding user to group %s...' % group)
        iam_client.add_user_to_group(GroupName = group, UserName = user)
        if user_info != None:
            user_info[user]['groups'].append(group)


def delete_user(iam_client, user, mfa_serial = None, keep_user = False, terminated_groups = []):
    """
    Delete IAM user

    :param iam_client:
    :param user:
    :param mfa_serial:
    :param keep_user:
    :param terminated_groups:
    :return:
    """
    printInfo('Deleting user %s...' % user)
    # Delete access keys
    try:
        aws_keys = get_access_keys(iam_client, user)
        for aws_key in aws_keys:
            try:
                printInfo('Deleting access key ID %s... ' % aws_key['AccessKeyId'], False)
                iam_client.delete_access_key(AccessKeyId = aws_key['AccessKeyId'], UserName = user)
                printInfo('Success')
            except Exception as e:
                printInfo('Failed')
                printException(e)
    except Exception as e:
        printException(e)
        printError('Failed to get access keys for user %s.' % user)
    # Deactivate and delete MFA devices
    try:
        mfa_devices = iam_client.list_mfa_devices(UserName = user)['MFADevices']
        for mfa_device in mfa_devices:
            serial = mfa_device['SerialNumber']
            try:
                printInfo('Deactivating MFA device %s... ' % serial, False)
                iam_client.deactivate_mfa_device(SerialNumber = serial, UserName = user)
                printInfo('Success')
            except Exception as e:
                printInfo('Failed')
                printException(e)
            delete_virtual_mfa_device(iam_client, serial)
        if mfa_serial:
            delete_virtual_mfa_device(iam_client, mfa_serial)
    except Exception as e:
        printException(e)
        printError('Failed to fetch MFA device serial number for user %s.' % user)
        pass
    # Remove IAM user from groups
    try:
        groups = iam_client.list_groups_for_user(UserName = user)['Groups']
        for group in groups:
            try:
                printInfo('Removing from group %s... ' % group['GroupName'], False)
                iam_client.remove_user_from_group(GroupName = group['GroupName'], UserName = user)
                printInfo('Success')
            except Exception as e:
                printInfo('Failed')
                printException(e)
    except Exception as e:
        printException(e)
        printError('Failed to fetch IAM groups for user %s.' % user)
        pass
    # Delete login profile
    login_profile = []
    try:
        login_profile = iam_client.get_login_profile(UserName = user)['LoginProfile']
    except Exception as e:
        pass
    try:
        if len(login_profile):
            printInfo('Deleting login profile... ', False)
            iam_client.delete_login_profile(UserName = user)
            printInfo('Success')
    except Exception as e:
        printInfo('Failed')
        printException(e)
        pass
    # Delete inline policies
    try:
        printInfo('Deleting inline policies... ', False)
        policies = iam_client.list_user_policies(UserName = user)
        for policy in policies['PolicyNames']:
            iam_client.delete_user_policy(UserName = user, PolicyName = policy)
        printInfo('Success')
    except Exception as e:
        printInfo('Failed')
        printException(e)
        pass
    # Detach managed policies
    try:
        printInfo('Detaching managed policies... ', False)
        policies = iam_client.list_attached_user_policies(UserName = user)
        for policy in policies['AttachedPolicies']:
            iam_client.detach_user_policy(UserName = user, PolicyArn = policy['PolicyArn'])
        printInfo('Success')
    except Exception as e:
        printInfo('Failed')
        printException(e)
    # Delete IAM user
    try:
        if not keep_user:
            iam_client.delete_user(UserName = user)
            printInfo('User %s deleted.' % user)
        else:
            for group in terminated_groups:
                add_user_to_group(iam_client, group, user)
    except Exception as e:
        printException(e)
        printError('Failed to delete user.')
        pass


def delete_virtual_mfa_device(iam_client, mfa_serial):
    """
    Delete a vritual MFA device given its serial number

    :param iam_client:
    :param mfa_serial:
    :return:
    """
    try:
        printInfo('Deleting MFA device %s...' % mfa_serial)
        iam_client.delete_virtual_mfa_device(SerialNumber = mfa_serial)
    except Exception as e:
        printException(e)
        printError('Failed to delete MFA device %s' % mfa_serial)
        pass

def get_access_keys(iam_client, user_name):
    """

    :param iam_client:
    :param user_name:
    :return:
    """
    keys = handle_truncated_response(iam_client.list_access_keys, {'UserName': user_name}, ['AccessKeyMetadata'])['AccessKeyMetadata']
    return keys


def show_access_keys(iam_client, user_name):
    """

    :param iam_client:
    :param user_name:
    :return:
    """
    keys = get_access_keys(iam_client, user_name)
    printInfo('User \'%s\' currently has %s access keys:' % (user_name, len(keys['AccessKeyMetadata'])))
    for key in keys['AccessKeyMetadata']:
        printInfo('\t%s (%s)' % (key['AccessKeyId'], key['Status']))


def init_iam_group_category_regex(category_groups, arg_category_regex):
    """
    Initialize and compile regular expression for category groups

    :param category_groups:
    :param arg_category_regex:
    :return:
    """
    if len(arg_category_regex) and len(category_groups) != len(arg_category_regex):
        printError('Error: you must provide as many regex as category groups.')
        return None
    else:
        category_regex = []
        for regex in arg_category_regex:
            if regex != '':
                category_regex.append(re.compile(regex))
            else:
                category_regex.append(None)
        return category_regex
