__author__ = 'pvde'

import lxml.etree
import logging

_NSMAP = {'cppa': 'http://docs.oasis-open.org/ebcore/ns/cppa/v3.0',
         'ds': 'http://www.w3.org/2000/09/xmldsig#',
         'xml': 'http://www.w3.org/XML/1998/namespace',
         'cppa2': 'http://www.oasis-open.org/committees/ebxml-cppa/schema/cpp-cpa-2_0.xsd',
         'xlink': 'http://www.w3.org/1999/xlink'
}

_CPPMODE = '_CPPMODE'
_CPAMODE = '_CPAMODE'

_USERMESSAGE = '_USERMESSAGE'
_SIGNALMESSAGE = '_SIGNALMESSAGE'

def cpp23(inputdoc):
    mode = None
    try:
        # in case we got an element tree
        cpp2doc = inputdoc.getroot()
    except:
        # in case we got an element
        cpp2doc = inputdoc
    if cpp2doc.tag == cppa2('CollaborationProtocolProfile'):
        mode = _CPPMODE
        outputdoc = lxml.etree.Element(cppa3('CPP'),
                                       nsmap= {'cppa': 'http://docs.oasis-open.org/ebcore/ns/cppa/v3.0',
                                               'ds': 'http://www.w3.org/2000/09/xmldsig#',
                                               'xml': 'http://www.w3.org/XML/1998/namespace' })
        return _cppa23(cpp2doc, outputdoc, mode=_CPPMODE)
    else:
        raise Exception(
            'Input document is not a CPP, root is {}, expecting {}'.format(cppa2doc.tag,
                                                                           cppa2('CollaborationProtocolProfile'))
        )

def cpa23(inputdoc):
    mode = None
    try:
        # in case we got an element tree
        cppa2doc = inputdoc.getroot()
    except:
        # in case we got an element
        cppa2doc = inputdoc
    if cppa2doc.tag == cppa2('CollaborationProtocolAgreement'):
        mode = _CPAMODE
        outputdoc = lxml.etree.Element(cppa3('CPA'),
                                       nsmap= {'cppa': 'http://docs.oasis-open.org/ebcore/ns/cppa/v3.0',
                                               'ds': 'http://www.w3.org/2000/09/xmldsig#',
                                               'xml': 'http://www.w3.org/XML/1998/namespace' })
        return _cppa23(cppa2doc, outputdoc, mode=_CPAMODE)
    else:
        raise Exception(
            'Input document is not a CPA, root is {}, expecting {}'.format(cppa2doc.tag,
                                                                           cppa2('CollaborationProtocolAgreement'))
        )

def _cppa23(inputdoc, outputdoc, mode=_CPPMODE):
    party_info = inputdoc.xpath('cppa2:PartyInfo',
                                namespaces=_NSMAP)[0]
    if mode == _CPPMODE:
        otherparty_info = None
    elif mode == _CPAMODE:
        otherparty_info = inputdoc.xpath('cppa2:PartyInfo',
                                         namespaces=_NSMAP)[1]
    map_parties(party_info, otherparty_info, outputdoc)
    matched_channels = {}
    matched_transports = {}
    match_collaborationroles(party_info, otherparty_info, outputdoc,
                             matched_channels, matched_transports, mode)
    for ch in matched_channels:
        outputdoc.append(matched_channels[ch])
    for tr in matched_transports:
        outputdoc.append(matched_transports[tr])
    return outputdoc

def map_parties(partyinfo, counterparty_info, parent):
    for (p, el) in [
        (partyinfo, cppa3('PartyInfo')),
        (counterparty_info, cppa3('CounterPartyInfo'))
        ]:
        if p != None:
            el = lxml.etree.SubElement(parent, el)
            map_party_elements(p, el)

def map_party_elements(inel, outel):
    v2_partyname = inel.get(cppa2('partyName'))
    v3_partyname = lxml.etree.SubElement(outel, cppa3('PartyName'))
    v3_partyname.text = v2_partyname

    v2_partyref = inel.xpath(
        'cppa2:PartyRef/@xlink:href',
        namespaces=_NSMAP
    )[0]
    v3_partyname.set('href', v2_partyref)
    v2_partyid = inel.xpath(
        'cppa2:PartyId',
        namespaces=_NSMAP
    )[0]
    v3_partyid = lxml.etree.SubElement(outel, cppa3('PartyId'))
    if v2_partyid.get(cppa2('type')) != None:
        v3_partyid.set('type', v2_partyid.get(cppa2('type')))



def match_collaborationroles(party_info, counterparty_info, parent,
                             matched_channels, matched_transports, mode):
    collaborationroles = party_info.xpath(
        'cppa2:CollaborationRole',
        namespaces = _NSMAP
    )
    for collaborationrole in collaborationroles:
        party_role = collaborationrole.xpath(
            'cppa2:Role/@cppa2:name',
            namespaces=_NSMAP
        )[0]
        process_specification = collaborationrole.xpath(
            'cppa2:ProcessSpecification',
            namespaces=_NSMAP
        )[0]
        process_name = process_specification.get(cppa2('name'))
        process_version = process_specification.get(cppa2('version'))
        process_uuid = process_specification.get(cppa2('uuid'))

        if mode == _CPAMODE:
            other_collaborationroles = counterparty_info.xpath(
                'cppa2:CollaborationRole',
                namespaces = _NSMAP
            )
            # In v2 PartyInfo we can only find the role of the other party
            # via the ActionBinding,  so we just try all of them.
            for othercollaborationrole in other_collaborationroles:
                counterparty_role = othercollaborationrole.xpath(
                    'cppa2:Role/@cppa2:name',
                    namespaces=_NSMAP
                )[0]
                service_specification_element = lxml.etree.Element(cppa3('ServiceSpecification'),
                                                                   name=process_name,
                                                                   version=process_version)
                if process_uuid != None:
                    service_specification_element.set('uuid',process_uuid)
                party_role_element = lxml.etree.SubElement(service_specification_element,
                                                           cppa3('PartyRole'))
                party_role_element.text = party_role
                counterparty_role_element = lxml.etree.SubElement(service_specification_element,
                                                                cppa3('CounterPartyRole'))
                counterparty_role_element.text= counterparty_role
                # A role pair is only added if there is at least one ServiceBinding
                # for the pair
                at_least_one_matching_servicebinding = False
                if match_servicebindings(collaborationrole, othercollaborationrole,
                    party_info, counterparty_info, service_specification_element,
                    matched_channels, matched_transports, mode):
                    parent.append(service_specification_element)
                else:
                    logging.info('No matching service bindings for {} {}'.format(party_role,
                                                                                 counterparty_role))
        elif mode == _CPPMODE:
            match_servicebindings(collaborationrole, None, counterparty_info,
                                  service_specification_element,
                                  matched_channels, matched_transports, mode)
        #
        #


def match_servicebindings(collaborationrole, othercollaborationrole, party_info, counterparty_info,
                          parent, matched_channels, matched_transports, mode):
    service_bindings = collaborationrole.xpath(
        'cppa2:ServiceBinding',
        namespaces=_NSMAP
    )
    at_least_one_matching_servicebinding = False
    for service_binding in service_bindings:
        service = service_binding.xpath(
            'cppa2:Service/text()',
            namespaces=_NSMAP
        )[0]
        service_binding_element = lxml.etree.SubElement(parent,
                                                        cppa3('ServiceBinding'))
        service_element = lxml.etree.SubElement(service_binding_element,
                                                cppa3('Service'))
        service_element.text = service
        if mode == _CPAMODE:
            other_servicebinding = othercollaborationrole.xpath(
                'cppa2:ServiceBinding[cppa2:Service/text()="{}"]'.format(service),
                namespaces=_NSMAP
            )[0]
        elif mode == _CPPMODE:
            other_servicebinding = None
        if match_actionbindings(party_info, service_binding, service,
            counterparty_info, other_servicebinding, service_binding_element,
            matched_channels, matched_transports, mode):
            at_least_one_matching_servicebinding = True
            match_actionbindings(party_info, service_binding, service,
                                 counterparty_info, other_servicebinding, parent,
                                 matched_channels, matched_transports, mode)
        else:
            logging.info('No matching service binding for {}'.format(service))
    return at_least_one_matching_servicebinding

def match_actionbindings(party_info, service_binding, service,
                         counterparty_info, other_servicebinding, parent,
                         matched_channels, matched_transports, mode):
    at_least_one_matching_actionbinding = False
    for (v2inbinding, send_or_receive, v2otherbindingxp) in [
        ('cppa2:CanSend','send','cppa2:CanReceive/cppa2:ThisPartyActionBinding[@cppa2:id="{}"]'),
        ('cppa2:CanReceive','receive','cppa2:CanSend/cppa2:ThisPartyActionBinding[@cppa2:id="{}"]')
    ]:
        for action_binding in service_binding.xpath(
            v2inbinding,
            namespaces=_NSMAP
        ):
            thispartyactionbinding = action_binding.xpath(
                'cppa2:ThisPartyActionBinding',
                namespaces = _NSMAP
            )[0]
            thisabid = thispartyactionbinding.xpath('@cppa2:id', namespaces=_NSMAP)[0]
            action = thispartyactionbinding.xpath('@cppa2:action', namespaces=_NSMAP)[0]
            channel_id = thispartyactionbinding.xpath('cppa2:ChannelId/text()', namespaces=_NSMAP)[0]
            actionbinding_element = lxml.etree.Element(cppa3('ActionBinding'),
                                                       sendOrReceive=send_or_receive,
                                                       action=action,
                                                       id=thisabid)
            ebbp_quality_attributes(thispartyactionbinding,
                                    actionbinding_element)
            action_context(thispartyactionbinding,
                           actionbinding_element)
            if mode == _CPAMODE:
                otherabid = action_binding.xpath(
                    'cppa2:OtherPartyActionBinding/text()',
                    namespaces = _NSMAP
                )[0]
                try:
                    xpq = v2otherbindingxp.format(otherabid)
                    otherpartyactionbinding = other_servicebinding.xpath(
                        xpq,
                        namespaces=_NSMAP
                    )[0]
                    otherchannel_id = otherpartyactionbinding.xpath(
                        'cppa2:ChannelId/text()',
                        namespaces=_NSMAP
                    )[0]
                    channelid_element = lxml.etree.SubElement(actionbinding_element,
                                                              cppa3('ChannelId'))
                    channelid_element.text = xrefid(channel_id, otherchannel_id, send_or_receive)
                except:
                    logging.info('{} {} no match in other party info'.format(thisabid, action))
                else:
                    at_least_one_matching_actionbinding = True
                    parent.append(actionbinding_element)
                    logging.info('{} {} {} {} {} {}'.format(thisabid, send_or_receive, action,
                                                            channel_id, otherabid, otherchannel_id))
            elif mode == _CPPMODE:
                parent.append(actionbinding_element)
                otherchannel_id = None
            match_channels(party_info, counterparty_info,
                           send_or_receive, channel_id, otherchannel_id, matched_channels, matched_transports)
    return at_least_one_matching_actionbinding

def ebbp_quality_attributes(thispartyactionbinding,
                            action_binding):
    business_transaction_characteristics = thispartyactionbinding.xpath(
        'cppa2:BusinessTransactionCharacteristics',
        namespaces=_NSMAP
    )[0]
    for att in ['isNonRepudiationRequired',
                'isNonRepudiationReceiptRequired',
                'isConfidential',
                'isAuthenticated',
                'isTamperProof',
                'isAuthorizationRequired',
                'isIntelligibleCheckRequired',
                'timeToAcknowledgeReceipt',
                'timeToAcknowledgeAcceptance',
                'timeToPerform',
                'retryCount']:
        value = business_transaction_characteristics.get(cppa2(att))
        logging.info('{} {} {}'.format(att, value, lxml.etree.tostring(business_transaction_characteristics)))
        if value != None:
            action_binding.set(att, value)

def action_context(thispartyactionbinding,
                   action_binding):
    action_context_list = thispartyactionbinding.xpath(
        'cppa2:ActionContext',
        namespaces=_NSMAP
    )
    if len(action_context_list) > 0:
        for (att) in ['binaryCollaboration',
                      'businessTransactionActivity',
                      'requestOrResponseAction']:
            value = action_context_list[0].get(cppa2(att))
            if value != None:
                action_binding.set(att, value)


def match_channels(party_info, counterparty_info, send_or_receive,
                   channel_id, otherchannel_id, matched_channels, matched_transports,
                   mode=_USERMESSAGE):
    this_v2_channel = party_info.xpath(
        'cppa2:DeliveryChannel[@cppa2:channelId="{}"]'.format(channel_id),
        namespaces=_NSMAP
    )[0]
    this_v2_messagingcharacteristics = this_v2_channel.xpath(
        'cppa2:MessagingCharacteristics',
        namespaces=_NSMAP
    )[0]
    this_v2_docexchange = this_v2_channel.xpath(
        '@cppa2:docExchangeId',
        namespaces=_NSMAP
    )[0]
    this_v2_transport = this_v2_channel.xpath(
        '@cppa2:transportId',
        namespaces=_NSMAP
    )[0]
    if otherchannel_id != None:
        other_v2_channel = counterparty_info.xpath(
            'cppa2:DeliveryChannel[@cppa2:channelId="{}"]'.format(otherchannel_id),
            namespaces=_NSMAP
        )[0]
        other_v2_messagingcharacteristics = other_v2_channel.xpath(
            'cppa2:MessagingCharacteristics',
            namespaces=_NSMAP
        )[0]
        other_v2_docexchange = other_v2_channel.xpath(
            '@cppa2:docExchangeId',
            namespaces=_NSMAP
        )[0]
        other_v2_transport = other_v2_channel.xpath(
            '@cppa2:transportId',
            namespaces=_NSMAP
        )[0]
    else:
        other_v2_channel = other_v2_docexchange = other_v2_transport =\
            other_v2_messagingcharacteristics = None
    matched_channel_id = xrefid(channel_id, otherchannel_id, send_or_receive, mode)
    matched_transport_id = xrefid(this_v2_transport, other_v2_transport, send_or_receive)
    ebms2_channel_element = lxml.etree.Element(cppa3('ebMS2Channel'),
                                               id=matched_channel_id,
                                               transport=matched_transport_id)
    if mode == _USERMESSAGE:
        signal_channel_id = signal_channel(party_info, counterparty_info,
                                           this_v2_messagingcharacteristics,
                                           send_or_receive,
                                           matched_channels, matched_transports)
        handle_error_handling(ebms2_channel_element, signal_channel_id)
        handle_receipt_handling(ebms2_channel_element, signal_channel_id,
                                this_v2_messagingcharacteristics)
        ebms_binding = get_ebxml_binding(party_info, this_v2_docexchange, send_or_receive)
        handle_reliable_messaging(ebms2_channel_element,
                                  this_v2_messagingcharacteristics,
                                  ebms_binding)
    matched_channels[matched_channel_id] = ebms2_channel_element
    match_transports(party_info, counterparty_info, send_or_receive,
                       this_v2_transport, other_v2_transport, matched_transports)

def signal_channel(party_info, counterparty_info,
                   messagingcharacteristics, send_or_receive,
                   matched_channels, matched_transports):
    sync_reply_mode = messagingcharacteristics.get(cppa2('syncReplyMode'), 'none')
    if sync_reply_mode in ['none', 'responseOnly']:
        # asynchronous signals
        channel_id = party_info.get(cppa2('defaultMshChannelId'))
        otherchannel_id = counterparty_info.get(cppa2('defaultMshChannelId'))
        match_channels(party_info, counterparty_info,
                       reverse(send_or_receive), channel_id, otherchannel_id,
                       matched_channels, matched_transports, mode=_SIGNALMESSAGE)
    return xrefid(channel_id, otherchannel_id, reverse(send_or_receive), _SIGNALMESSAGE)

def handle_error_handling(ebms2_channel_element, signal_channel_id):
    error_handling_element = lxml.etree.SubElement(ebms2_channel_element,
                                                   cppa3('ErrorHandling'))
    receiver_errors_channel_element = lxml.etree.SubElement(error_handling_element,
                                                            cppa3('ReceiverErrorsReportChannelId'))
    receiver_errors_channel_element.text = signal_channel_id

def handle_receipt_handling(ebms2_channel_element, signal_channel_id, messagingcharacteristics):
    ackrequested = messagingcharacteristics.get(cppa2('ackRequested'), 'perMessage')
    if ackrequested != 'never':
        receipt_handling_element = lxml.etree.SubElement(ebms2_channel_element,
                                                         cppa3('ReceiptHandling'))
        receipt_channel_element = lxml.etree.SubElement(receipt_handling_element,
                                                        cppa3('ReceiptChannelId'))
        receipt_channel_element.text = signal_channel_id

def handle_reliable_messaging(ebms2_channel_element, messagingcharacteristics, ebmsbinding):
    duplicate_elimination = messagingcharacteristics.get(cppa2('ackRequested'), 'perMessage')

    ebms_rm_list = ebmsbinding.xpath(
        'cppa2:ReliableMessaging',
        namespaces=_NSMAP
    )

    if duplicate_elimination != 'never' or len(ebms_rm_list) > 0:
        rm_element = lxml.etree.SubElement(ebms2_channel_element,
                                           cppa3('ebMS2ReliableMessaging'))
        actor = messagingcharacteristics.get(cppa2('actor'))
        if actor != None:
            rm_element.set('actor', actor)
        if duplicate_elimination != 'never':
            dh_element = lxml.etree.SubElement(rm_element,
                                               cppa3('DuplicateHandling'))
            de_element = lxml.etree.SubElement(dh_element,
                                               cppa3('DuplicateElimination'))
            de_element.text = 'true'
        if len(ebms_rm_list) > 0:
            ebms_rm = ebms_rm_list[0]
            logging.info(lxml.etree.tostring(ebms_rm))
            rh_element = lxml.etree.SubElement(rm_element,
                                               cppa3('RetryHandling'))
            try:
                retries = ebms_rm.xpath('cppa2:Retries/text()', namespaces=_NSMAP)[0]
                retries_element = lxml.etree.SubElement(rh_element,
                                                        cppa3('Retries'))
                retries_element.text = retries
            except:
                pass
            try:
                retry_int = ebms_rm.xpath('cppa2:RetryInterval/text()', namespaces=_NSMAP)[0]
                retry_int_element = lxml.etree.SubElement(rh_element,
                                                        cppa3('RetryInterval'))
                retry_int_element.text = retry_int
            except:
                pass
            message_ordering = ebms_rm.xpath('cppa2:MessageOrderSemantics/text()', namespaces=_NSMAP)[0]
            if message_ordering == 'Guaranteed':
                rm_element.set('ordered', 'true')
            else:
                rm_element.set('ordered', 'false')



def get_ebxml_binding(party_info, docexchangeid, send_or_receive):
    if send_or_receive == 'send':
        return party_info.xpath(
            'cppa2:DocExchange[@cppa2:docExchangeId="{}"]/cppa2:ebXMLSenderBinding'.format(docexchangeid),
            namespaces=_NSMAP
        )[0]
    else:
        return party_info.xpath(
            'cppa2:DocExchange[@cppa2:docExchangeId="{}"]/cppa2:ebXMLReceiverBinding'.format(docexchangeid),
            namespaces=_NSMAP
        )[0]



def xrefid(v1, v2, v3, v4=_USERMESSAGE):
    if v4 == _SIGNALMESSAGE:
        return '{}_{}_{}{}'.format(v1, v2, v3, v4)
    else:
        return '{}_{}_{}'.format(v1, v2, v3)

def reverse(direction):
    if direction == 'send':
        return 'receive'
    elif direction == 'receive':
        return 'send'

def match_transports(party_info, counterparty_info, send_or_receive,
                     transport_id, othertransport_id, matched_transports):
    if send_or_receive == 'send':
        sender_transport = party_info.xpath(
            'cppa2:Transport[@cppa2:transportId="{}"]/cppa2:TransportSender'.format(transport_id),
            namespaces=_NSMAP
        )[0]
        receiver_transport = counterparty_info.xpath(
            'cppa2:Transport[@cppa2:transportId="{}"]/cppa2:TransportReceiver'.format(othertransport_id),
            namespaces=_NSMAP
        )[0]
    else:
        receiver_transport = party_info.xpath(
            'cppa2:Transport[@cppa2:transportId="{}"]/cppa2:TransportReceiver'.format(transport_id),
            namespaces=_NSMAP
        )[0]
        sender_transport = counterparty_info.xpath(
            'cppa2:Transport[@cppa2:transportId="{}"]/cppa2:TransportSender'.format(othertransport_id),
            namespaces=_NSMAP
        )[0]
    transport_protocol = sender_transport.xpath(
        'cppa2:TransportProtocol',
        namespaces=_NSMAP
    )[0]
    transport_protocol_name = transport_protocol.text
    transport_protocol_version_list = transport_protocol.xpath(
        '@cppa2:version',
        namespaces=_NSMAP
    )
    if transport_protocol_name == 'HTTP':
        unified_transport = lxml.etree.Element('HTTPTransport',
                                               id=xrefid(transport_id,
                                                         othertransport_id,
                                                         send_or_receive))
    elif transport_protocol_name == 'SMTP':
        unified_transport = lxml.etree.Element('SMTPTransport')
    if len(transport_protocol_version_list) > 0:
        unified_transport.set('version', transport_protocol_version_list[0])

    endpoint_element = lxml.etree.SubElement(unified_transport,
                                             cppa3('Endpoint'))
    endpoint_element.text = receiver_transport.xpath(
        'cppa2:Endpoint/@cppa2:uri', namespaces=_NSMAP
    )[0]

    matched_transports[xrefid(transport_id,
                              othertransport_id,
                              send_or_receive)] = unified_transport

def cppa3(el):
    return '{{{}}}{}'.format(_NSMAP['cppa'],el)

def cppa2(el):
    return '{{{}}}{}'.format(_NSMAP['cppa2'],el)

