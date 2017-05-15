# -*- coding: utf-8 -*-
"""
:copyright: (c) 2015 - 2017 Stichting Koppeltaal
:license: AGPL, see `LICENSE.md` for more details.
"""

import datetime
import mock
import pytest
import zope.interface.verify
import koppeltaal.codes
import koppeltaal.definitions
import koppeltaal.fhir.packer
import koppeltaal.fhir.resource
import koppeltaal.interfaces
import koppeltaal.models
import koppeltaal.utils


@pytest.fixture
def packer():
    return koppeltaal.fhir.packer.Packer(
        mock.MagicMock(
            **{'spec': koppeltaal.fhir.resource.Resource,
               'find.return_value': None}),
        mock.MagicMock(return_value='https://example.com/dummy/dummy'))


@pytest.fixture
def NAMESPACE():
    return koppeltaal.interfaces.NAMESPACE


def test_coding(packer, NAMESPACE):

    vertebrates = koppeltaal.codes.Code(
        'Vertebrate',
        ['amphibians',
         'birds',
         'mammals',
         'reptiles'])

    packed = vertebrates.pack_code('amphibians')
    assert packed == 'amphibians'

    with pytest.raises(koppeltaal.interfaces.InvalidCode):
        vertebrates.pack_code('sponges')

    coding = vertebrates.pack_coding('amphibians')
    assert coding == {
        'code': 'amphibians',
        'display': 'amphibians',
        'system': NAMESPACE + 'Vertebrate'}

    with pytest.raises(koppeltaal.interfaces.InvalidCode):
        vertebrates.pack_coding('sponges')

    unpacked = vertebrates.unpack_code('amphibians')
    assert unpacked == 'amphibians'

    with pytest.raises(koppeltaal.interfaces.InvalidCode):
        vertebrates.unpack_code('sponges')

    unpacked_coding = vertebrates.unpack_coding({
        'code': 'amphibians',
        'display': 'amphibians',
        'system': NAMESPACE + 'Vertebrate'})

    assert 'amphibians' == unpacked_coding

    with pytest.raises(koppeltaal.interfaces.InvalidCode):
        vertebrates.unpack_coding({
            'code': 'sponges',
            'display': 'sponges',
            'system': NAMESPACE + 'Vertebrate'})

    unknown_value = vertebrates.unpack_coding({
        'code': 'UNK',
        'display': 'Unkown',
        'system': koppeltaal.codes.NULL_SYSTEM})

    assert unknown_value is None

    with pytest.raises(koppeltaal.interfaces.InvalidCode):
        vertebrates.unpack_coding({
            'code': 'UNKNOW',
            'display': 'Unkown',
            'system': koppeltaal.codes.NULL_SYSTEM})

    with pytest.raises(koppeltaal.interfaces.InvalidSystem):
        vertebrates.unpack_coding({
            'code': 'reptiles',
            'display': 'reptiles',
            'system': 'foobarbaz'})


def test_unpack_name(packer):
    name = packer.unpack(
        {'given': [u'Napoleon'],
         'family': [u'Bonaparte'],
         'use': u'official'},
        koppeltaal.definitions.Name)
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Name, name)
    assert name.given == [u'Napoleon']
    assert name.family == [u'Bonaparte']
    assert name.use == 'official'

    name = packer.unpack(
        {'given': [u'Thea'],
         'family': [u'van', u'de', u'Bovenburen'],
         'suffix': [u'van', u'den', u'Overkant'],
         'use': u'official'},
        koppeltaal.definitions.Name)
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Name, name)
    assert name.given == [u'Thea']
    assert name.family == [u'van', u'de', u'Bovenburen']
    assert name.suffix == [u'van', u'den', u'Overkant']
    assert name.use == 'official'


def test_pack_name(packer):
    name1 = packer.pack(
        koppeltaal.models.Name(
            given=[u'Napoleon'],
            family=[u'Bonaparte'],
            use='old'),
        koppeltaal.definitions.Name)

    assert name1 == {
        'family': ['Bonaparte'],
        'given': ['Napoleon'],
        'id': mock.ANY,
        'use': 'old'}

    name2 = packer.pack(
        koppeltaal.models.Name(
            given=[u'Nathan']),
        koppeltaal.definitions.Name)

    assert name2 == {
        'given': ['Nathan'],
        'id': mock.ANY,
        'use': 'official'}

    name3 = packer.pack(
        koppeltaal.models.Name(
            given=[u'Nathan'],
            family=[u'der', u'Fantasten'],
            suffix=[u'tot', u'Daarhelemaalië']),
        koppeltaal.definitions.Name)

    assert name3 == {
        'given': ['Nathan'],
        'family': [u'der', u'Fantasten'],
        'id': mock.ANY,
        'suffix': [u'tot', u'Daarhelemaalië'],
        'use': 'official'}

    with pytest.raises(koppeltaal.interfaces.InvalidResource):
        packer.pack(
            'Napoleon',
            koppeltaal.definitions.Name)

    with pytest.raises(koppeltaal.interfaces.InvalidValue):
        packer.pack(
            koppeltaal.models.Name(
                given=[u'Napoleon'],
                family=[u'Bonaparte'],
                use='cool name'),
            koppeltaal.definitions.Name)


def test_unpack_patient(packer, NAMESPACE):
    patient1 = packer.unpack(
        {'active': True,
         'extension': [
             {'url': NAMESPACE + u'Patient#Age',
              'valueInteger': 42}],
         'gender': {'coding': [
             {'code': u'M',
              'display': u'M',
              'system': u'http://hl7.org/fhir/v3/AdministrativeGender'}]},
         'name': [
             {'given': [u'Paul'],
              'family': [u'Roger'],
              'use': u'official'}]},
        koppeltaal.definitions.Patient)

    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Patient, patient1)
    name = patient1.name[0]
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Name, name)
    assert name.given == [u'Paul']
    assert name.family == [u'Roger']
    assert name.use == 'official'
    assert len(patient1.contacts) == 0
    assert len(patient1.identifiers) == 0
    assert patient1.age == 42
    assert patient1.active is True
    assert patient1.birth_date is None
    assert patient1.gender == 'M'

    patient2 = packer.unpack(
        {'gender': {'coding': [
            {'code': u'UNK',
             'display': u'UNK',
             'system': u'http://hl7.org/fhir/v3/NullFlavor'}]},
         'name': [
             {'given': [u'Paul'],
              'family': [u'Roger'],
              'use': u'official'}]},
        koppeltaal.definitions.Patient)
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Patient, patient2)
    name2 = patient2.name[0]
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Name, name2)
    assert name2.given == [u'Paul']
    assert name2.family == [u'Roger']
    assert name2.use == 'official'
    assert len(patient2.contacts) == 0
    assert len(patient2.identifiers) == 0
    assert patient2.age is None
    assert patient2.active is None
    assert patient2.birth_date is None
    assert patient2.gender is None


def test_pack_patient(packer):
    patient1 = packer.pack(
        koppeltaal.models.Patient(
            active=True,
            age=42,
            name=[
                koppeltaal.models.Name(
                    given=[u'Paul'],
                    family=[u'Roger'],
                    use='official')],
            gender='M'),
        koppeltaal.definitions.Patient)

    assert patient1 == {
        'active': True,
        'extension': [
            {'url': 'http://ggz.koppeltaal.nl/fhir/Koppeltaal/Patient#Age',
             'valueInteger': 42}],
        'id': mock.ANY,
        'gender': {'coding': [
            {'code': 'M',
             'display': 'M',
             'system': 'http://hl7.org/fhir/v3/AdministrativeGender'}]},
        'name': [
            {'id': mock.ANY,
             'given': ['Paul'],
             'family': ['Roger'],
             'use': 'official'}]}

    patient2 = packer.pack(
        koppeltaal.models.Patient(
            birth_date=datetime.datetime(1976, 6, 1, 12, 34),
            contacts=[
                koppeltaal.models.Contact(
                    system='email',
                    value=u'petra@example.com',
                    use='home')],
            identifiers=[
                koppeltaal.models.Identifier(
                    system=u'http://fhir.nl/fhir/NamingSystem/bsn',
                    value=u'640563569',
                    use='official')],
            name=[
                koppeltaal.models.Name(
                    given=[u'Petra'],
                    use='temp')],
            gender='F'),
        koppeltaal.definitions.Patient)

    assert patient2 == {
        'birthDate': '1976-06-01T12:34:00',
        'gender': {'coding': [
            {'code': 'F',
             'display': 'F',
             'system': 'http://hl7.org/fhir/v3/AdministrativeGender'}]},
        'id': mock.ANY,
        'identifier': [
            {'id': mock.ANY,
             'system': 'http://fhir.nl/fhir/NamingSystem/bsn',
             'value': '640563569',
             'use': 'official'}],
        'name': [
            {'id': mock.ANY,
             'given': ['Petra'],
             'use': 'temp'}],
        'telecom': [
            {'id': mock.ANY,
             'system': 'email',
             'value': 'petra@example.com',
             'use': 'home'}]}


def test_unpack_practitioner(packer):
    practitioner1 = packer.unpack(
        {'telecom': [
            {'system': u'email',
             'value': u'paul@example.com',
             'use': u'work'}],
         'name':  {'given': [u'Paul'],
                   'family': [u'Cézanne'],
                   'use': u'official'}},
        koppeltaal.definitions.Practitioner)

    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Practitioner, practitioner1)
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Name, practitioner1.name)
    assert practitioner1.name.given == [u'Paul']
    assert practitioner1.name.family == [u'Cézanne']
    assert practitioner1.name.use == 'official'
    assert len(practitioner1.contacts) == 1
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.Contact, practitioner1.contacts[0])
    assert practitioner1.contacts[0].system == 'email'
    assert practitioner1.contacts[0].value == u'paul@example.com'
    assert practitioner1.contacts[0].use == 'work'
    assert len(practitioner1.identifiers) == 0


def test_pack_practitioner(packer):
    practitioner1 = packer.pack(
        koppeltaal.models.Practitioner(
            contacts=[
                koppeltaal.models.Contact(
                    system='email',
                    value=u'paul@example.com',
                    use='work')],
            identifiers=[
                koppeltaal.models.Identifier(
                    system=u'http://fhir.nl/fhir/NamingSystem/bsn',
                    value=u'154694496',
                    use='official')],
            name=koppeltaal.models.Name(
                given=[u'Paul'],
                family=[u'Cézanne'])),
        koppeltaal.definitions.Practitioner)

    assert practitioner1 == {
        'id': mock.ANY,
        'identifier': [
            {'id': mock.ANY,
             'system': 'http://fhir.nl/fhir/NamingSystem/bsn',
             'value': '154694496',
             'use': 'official'}],
        'name': {'id': mock.ANY,
                 'given': ['Paul'],
                 'family': [u'Cézanne'],
                 'use': 'official'},
        'telecom': [
            {'id': mock.ANY,
             'system': 'email',
             'value': 'paul@example.com',
             'use': 'work'}]}


def test_unpack_activity_definition(packer, NAMESPACE):
    definition1 = packer.unpack(
        {'extension': [
            {'url': (NAMESPACE +
                     u'ActivityDefinition#ActivityDefinitionIdentifier'),
             'valueString': u'myapp'},
            {'url': NAMESPACE + u'ActivityDefinition#ActivityName',
             'valueString': u'My APP'},
            {'url': NAMESPACE + u'ActivityDefinition#ActivityKind',
             'valueCoding': {
                 'code': u'Game',
                 'display': u'Game',
                 'system': NAMESPACE + u'ActivityKind'}},
            {'url': NAMESPACE + u'ActivityDefinition#Application',
             'valueResource': {
                 'reference': 'https://example.com/refmyapp',
                 'display': u'refmyapp'}}]},
        koppeltaal.definitions.ActivityDefinition)

    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.ActivityDefinition, definition1)
    assert definition1.identifier == 'myapp'
    assert definition1.name == 'My APP'
    assert definition1.kind == 'Game'
    assert zope.interface.verify.verifyObject(
        koppeltaal.interfaces.IReferredFHIRResource, definition1.application)
    assert definition1.application.fhir_link == 'https://example.com/refmyapp'
    assert definition1.application.display == 'refmyapp'
    assert definition1.launch_type == 'Web'
    assert definition1.is_active is True
    assert definition1.is_domain_specific is None
    assert definition1.is_archived is False
    assert len(definition1.subactivities) == 0


def test_unpack_message_header(packer, NAMESPACE):
    message1 = packer.unpack(
        {'data': [{'reference': 'https://example.com/data'}],
         'event': {'code': u'CreateOrUpdatePatient',
                   'display': u'CreateOrUpdatePatient',
                   'system': NAMESPACE + u'MessageEvents'},
         'identifier': u'42-42-42',
         'source': {'name': u'unpack message header',
                    'version': u'about 1.0',
                    'endpoint': u'https://example.com/here',
                    'software': u'pytest'},
         'timestamp': u'2015-10-09T12:16:00+00:00'},
        koppeltaal.definitions.MessageHeader)

    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.MessageHeader, message1)
    assert zope.interface.verify.verifyObject(
        koppeltaal.interfaces.IReferredFHIRResource, message1.data)
    assert message1.data.fhir_link == 'https://example.com/data'
    assert message1.event == 'CreateOrUpdatePatient'
    assert message1.identifier == '42-42-42'
    assert zope.interface.verify.verifyObject(
        koppeltaal.definitions.MessageHeaderSource, message1.source)
    assert message1.source.endpoint == 'https://example.com/here'
    assert message1.source.name == 'unpack message header'
    assert message1.source.software == 'pytest'
    assert message1.source.version == 'about 1.0'
    assert message1.timestamp == datetime.datetime(
        2015, 10, 9, 12, 16, tzinfo=koppeltaal.utils.utc)


def test_pack_message_header(packer, NAMESPACE):
    message1 = packer.pack(
        koppeltaal.models.MessageHeader(
            timestamp=datetime.datetime(2015, 10, 9, 12, 4),
            event='CreateOrUpdatePatient',
            identifier=u'42-42',
            source=koppeltaal.models.MessageHeaderSource(
                software=u"pytest",
                endpoint=u'https://example.com/here')),
        koppeltaal.definitions.MessageHeader)

    assert message1 == {
        'event': {'code': 'CreateOrUpdatePatient',
                  'display': 'CreateOrUpdatePatient',
                  'system': NAMESPACE + 'MessageEvents'},
        'id': mock.ANY,
        'identifier': u'42-42',
        'source': {'endpoint': u'https://example.com/here',
                   'id': mock.ANY,
                   'software': u'pytest'},
        'timestamp': '2015-10-09T12:04:00+00:00'}


def test_unpack_extension_invalid_integer(packer, NAMESPACE):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'extension': [
                {'url': NAMESPACE + u'Patient#Age',
                 'valueInteger': u'forty'}],
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'age'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'extension': [
                {'url': NAMESPACE + u'Patient#Age',
                 'value': 40}],
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'age'."


def test_unpack_extension_required_missing(packer, NAMESPACE):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'extension': [
                {'url': (NAMESPACE +
                         u'ActivityDefinition#ActivityDefinitionIdentifier'),
                 'valueString': u'myapp'},
                {'url': NAMESPACE + u'ActivityDefinition#ActivityName',
                 'valueString': u'My APP'},
                {'url': NAMESPACE + u'ActivityDefinition#ActivityKind',
                 'valueCoding': {
                     'code': u'Game',
                     'display': u'Game',
                     'system': NAMESPACE + u'ActivityKind'}}]},
            koppeltaal.definitions.ActivityDefinition)
    assert str(error.value) == \
        "RequiredMissing: 'application' required but missing."


def test_unpack_native_invalid_boolean(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'active': u'yes!',
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'active'."


def test_unpack_native_invalid_code(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidCode) as error:
        packer.unpack(
            {'use': u'cool name'},
            koppeltaal.definitions.Name)
    assert str(error.value) == \
        "InvalidCode: 'cool name' not in 'http://hl7.org/fhir/name-use'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'use': None},
            koppeltaal.definitions.Name)
    assert str(error.value) == \
        "InvalidValue: invalid value for 'use'."


def test_unpack_native_invalid_coding(packer, NAMESPACE):
    with pytest.raises(koppeltaal.interfaces.InvalidCode) as error:
        packer.unpack(
            {'event': {'code': u'CreateWorld',
                       'display': u'CreateWorld',
                       'system': NAMESPACE + u'MessageEvents'},
             'identifier': u'42-42-42',
             'source': {'endpoint': u'https://example.com/here',
                        'software': u'pytest'},
             'timestamp': u'2015-10-09T12:16:00+00:00'},
            koppeltaal.definitions.MessageHeader)
    assert str(error.value) == \
        "InvalidCode: 'CreateWorld' not in " \
        "'http://ggz.koppeltaal.nl/fhir/Koppeltaal/MessageEvents'."

    with pytest.raises(koppeltaal.interfaces.InvalidCode) as error:
        packer.unpack(
            {'event': {'coding': u'CreateOrUpdatePatient',
                       'system': NAMESPACE + u'MessageEvents'},
             'identifier': u'42-42-42',
             'source': {'endpoint': u'https://example.com/here',
                        'software': u'pytest'},
             'timestamp': u'2015-10-09T12:16:00+00:00'},
            koppeltaal.definitions.MessageHeader)
    assert str(error.value) == \
        "InvalidCode: code is missing."

    with pytest.raises(koppeltaal.interfaces.InvalidSystem) as error:
        packer.unpack(
            {'event': {'code': u'CreateWorld',
                       'display': u'CreateWorld',
                       'system': u'http://example.com/event'},
             'identifier': u'42-42-42',
             'source': {'endpoint': u'https://example.com/here',
                        'software': u'pytest'},
             'timestamp': u'2015-10-09T12:16:00+00:00'},
            koppeltaal.definitions.MessageHeader)
    assert str(error.value) == \
        "InvalidSystem: system 'http://example.com/event' is not supported."

    with pytest.raises(koppeltaal.interfaces.InvalidSystem) as error:
        packer.unpack(
            {'event': {'code': u'CreateOrUpdatePatient'},
             'identifier': u'42-42-42',
             'source': {'endpoint': u'https://example.com/here',
                        'software': u'pytest'},
             'timestamp': u'2015-10-09T12:16:00+00:00'},
            koppeltaal.definitions.MessageHeader)
    assert str(error.value) == \
        "InvalidSystem: system is missing."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'event': u'CreateOrUpdatePatient',
             'identifier': u'42-42-42',
             'source': {'endpoint': u'https://example.com/here',
                        'software': u'pytest'},
             'timestamp': u'2015-10-09T12:16:00+00:00'},
            koppeltaal.definitions.MessageHeader)
    assert str(error.value) == \
        "InvalidValue: invalid value for 'event'."


def test_unpack_native_invalid_datetime(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'birthDate': u'yesterday',
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'birthDate'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'birthDate': -1,
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'birthDate'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'birthDate': False,
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'birthDate'."


def test_unpack_native_invalid_multiple(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'given': u'Napoleon'},
            koppeltaal.definitions.Name)
    assert str(error.value) == "InvalidValue: invalid value for 'given'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'family': 42},
            koppeltaal.definitions.Name)
    assert str(error.value) == "InvalidValue: invalid value for 'family'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'family': [42]},
            koppeltaal.definitions.Name)
    assert str(error.value) == "InvalidValue: invalid value for 'family'."


def test_unpack_native_invalid_object(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'telecom': u'by fax',
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'telecom'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'telecom': False,
             'name': [{'given': [u'Me']}]},
            koppeltaal.definitions.Patient)
    assert str(error.value) == "InvalidValue: invalid value for 'telecom'."


def test_unpack_native_invalid_string(packer):
    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'value': 42},
            koppeltaal.definitions.Identifier)
    assert str(error.value) == "InvalidValue: invalid value for 'value'."

    with pytest.raises(koppeltaal.interfaces.InvalidValue) as error:
        packer.unpack(
            {'value': True},
            koppeltaal.definitions.Identifier)
    assert str(error.value) == "InvalidValue: invalid value for 'value'."


def test_unpack_allow_broken(packer):
    broken = packer.unpack(
        {'use': u'cool name'},
        koppeltaal.definitions.Name,
        allow_broken=True)
    assert not koppeltaal.definitions.Name.providedBy(broken)
    assert zope.interface.verify.verifyObject(
        koppeltaal.interfaces.IBrokenFHIRResource, broken)
    assert str(broken.error) == \
        "InvalidCode: 'cool name' not in 'http://hl7.org/fhir/name-use'."
