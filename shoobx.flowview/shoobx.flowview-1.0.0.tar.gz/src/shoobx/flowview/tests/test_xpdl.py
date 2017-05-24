###############################################################################
#
# Copyright 2014 by Shoobx, Inc.
#
###############################################################################
import os
import re

from shoobx.flowview import xpdl


def test_transform_to_html():
    here = os.path.dirname(__file__)
    samples_dir = os.path.join(here, 'samples')

    output = xpdl.transform_to_html(os.path.join(samples_dir, "samples.xpdl"))

    assert output.startswith('<!DOCTYPE html>')

    processes = re.findall('<h2.*?>(.*?) <small>.*?</h2>', output)
    assert processes == [
        'Schedule Process',
        'Scheduled Process',
        'Schedule Message Delivery',
        'Multi-Participant Subprocess',
        'Sub-Process',
        'Crash',
        'Event listener',
        'Delay Process',
        'Subflow Master Process',
        'Conditional Transitions',
        'Sample Subflow'
    ]
