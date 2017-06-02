# -*- coding: utf-8 -*-
from colorama.initialise import init

from specpie.spec import should, spec

from specpie.fake_decorator import FakeDecorator

from specpie.descriptors import describe, context, it

init()

should = should
describe = describe
context = context
it = it
spec = spec
fake = FakeDecorator
