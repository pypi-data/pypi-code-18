# Copyright 2017 Real ReadMe Limited <epp@realread.me>. All Rights Reserved.
# Copyright 2017 Eduardo A. Paris Penas <edward2a@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Deep Dict Merge.

Recursively merge dictionaries and return the result.
"""


__author__ = 'Eduardo A. Paris Penas'
__version__ = '0.1'


def deep_merge(base, changes):
    """
    Create a copy of ``base`` dict and recursively merges the ``changes`` dict.

    Returns merged dict.

    :type base: dict
    :param base: The base dictionary for the merge
    :type changes: dict
    :param changes: The dictionary to merge into the base one
    :return: The merged ``result`` dict
    """
    def merge(result, changes):
        for k, v in changes.items():
            if not isinstance(v, dict):
                result[k] = v
            else:
                if k not in result or not isinstance(result[k], dict):
                    result[k] = v.copy()
                else:
                    result[k] = result[k].copy()
                    merge(result[k], changes[k])

    result = base.copy()
    merge(result, changes)
    return result

