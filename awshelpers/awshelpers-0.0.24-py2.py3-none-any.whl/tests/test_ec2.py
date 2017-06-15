from awshelpers.ec2 import describe as ec2_describe

AWSHELPERS_NETWORK_INTERFACE = 'eni-3b630110'


def test():
    """
    Lookup a known elastic IP
    
    :return: None
    :rtype: None
    """
    assert len(ec2_describe.eip_addresses([AWSHELPERS_NETWORK_INTERFACE], 'PublicIp')) >= 1
