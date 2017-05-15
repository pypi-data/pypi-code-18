# encoding: utf-8
"""
icmp.py

Created by Thomas Mangin on 2010-01-15.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.protocol.resource import Resource


# ============================================================== ICMP Code Field
# https://www.iana.org/assignments/icmp-parameters

class ICMPType (Resource):
	NAME = 'icmp type'

	ECHO_REPLY               = 0x00
	# DESTINATION_UNREACHEABLE = 0x03
	UNREACHABLE              = 0x03
	SOURCE_QUENCH            = 0x04
	REDIRECT                 = 0x05
	ECHO_REQUEST             = 0x08
	ROUTER_ADVERTISEMENT     = 0x09
	ROUTER_SOLICIT           = 0x0A
	TIME_EXCEEDED            = 0x0B
	PARAMETER_PROBLEM        = 0x0C
	TIMESTAMP                = 0x0D
	TIMESTAMP_REPLY          = 0x0E
	INFO_REQUEST             = 0x0F
	INFO_REPLY               = 0x10
	MASK_REQUEST             = 0x11
	MASK_REPLY               = 0x12
	TRACEROUTE               = 0x1E

	codes = dict ((k.lower().replace('_','-'),v) for (k,v) in {
		'ECHO_REPLY':               ECHO_REPLY,
		'UNREACHABLE':              UNREACHABLE,
		'SOURCE_QUENCH':            SOURCE_QUENCH,
		'REDIRECT':                 REDIRECT,
		'ECHO_REQUEST':             ECHO_REQUEST,
		'ROUTER_ADVERTISEMENT':     ROUTER_ADVERTISEMENT,
		'ROUTER_SOLICIT':           ROUTER_SOLICIT,
		'TIME_EXCEEDED':            TIME_EXCEEDED,
		'PARAMETER_PROBLEM':        PARAMETER_PROBLEM,
		'TIMESTAMP':                TIMESTAMP,
		'TIMESTAMP_REPLY':          TIMESTAMP_REPLY,
		'INFO_REQUEST':             INFO_REQUEST,
		'INFO_REPLY':               INFO_REPLY,
		'MASK_REQUEST':             MASK_REQUEST,
		'MASK_REPLY':               MASK_REPLY,
		'TRACEROUTE':               TRACEROUTE,
	}.items())

	names = dict([(r,l) for (l,r) in codes.items()])


# https://www.iana.org/assignments/icmp-parameters
class ICMPCode (Resource):
	NAME = 'icmp code'

	# Destination Unreacheable (type 3)
	NETWORK_UNREACHABLE                   = 0x0
	HOST_UNREACHABLE                      = 0x1
	PROTOCOL_UNREACHABLE                  = 0x2
	PORT_UNREACHABLE                      = 0x3
	FRAGMENTATION_NEEDED                  = 0x4
	SOURCE_ROUTE_FAILED                   = 0x5
	DESTINATION_NETWORK_UNKNOWN           = 0x6
	DESTINATION_HOST_UNKNOWN              = 0x7
	SOURCE_HOST_ISOLATED                  = 0x8
	DESTINATION_NETWORK_PROHIBITED        = 0x9
	DESTINATION_HOST_PROHIBITED           = 0xA
	NETWORK_UNREACHABLE_FOR_TOS           = 0xB
	HOST_UNREACHABLE_FOR_TOS              = 0xC
	COMMUNICATION_PROHIBITED_BY_FILTERING = 0xD
	HOST_PRECEDENCE_VIOLATION             = 0xE
	PRECEDENCE_CUTOFF_IN_EFFECT           = 0xF

	# Redirect (Type 5)
	REDIRECT_FOR_NETWORK                  = 0x0
	REDIRECT_FOR_HOST                     = 0x1
	REDIRECT_FOR_TOS_AND_NET              = 0x2
	REDIRECT_FOR_TOS_AND_HOST             = 0x3

	# Time Exceeded (Type 11)
	TTL_EQ_ZERO_DURING_TRANSIT            = 0x0
	TTL_EQ_ZERO_DURING_REASSEMBLY         = 0x1

	# parameter Problem (Type 12)
	REQUIRED_OPTION_MISSING               = 0x1
	IP_HEADER_BAD                         = 0x2

	codes = dict ((k.lower().replace('_','-'),v) for (k,v) in {
		'NETWORK_UNREACHABLE':                   NETWORK_UNREACHABLE,
		'HOST_UNREACHABLE':                      HOST_UNREACHABLE,
		'PROTOCOL_UNREACHABLE':                  PROTOCOL_UNREACHABLE,
		'PORT_UNREACHABLE':                      PORT_UNREACHABLE,
		'FRAGMENTATION_NEEDED':                  FRAGMENTATION_NEEDED,
		'SOURCE_ROUTE_FAILED':                   SOURCE_ROUTE_FAILED,
		'DESTINATION_NETWORK_UNKNOWN':           DESTINATION_NETWORK_UNKNOWN,
		'DESTINATION_HOST_UNKNOWN':              DESTINATION_HOST_UNKNOWN,
		'SOURCE_HOST_ISOLATED':                  SOURCE_HOST_ISOLATED,
		'DESTINATION_NETWORK_PROHIBITED':        DESTINATION_NETWORK_PROHIBITED,
		'DESTINATION_HOST_PROHIBITED':           DESTINATION_HOST_PROHIBITED,
		'NETWORK_UNREACHABLE_FOR_TOS':           NETWORK_UNREACHABLE_FOR_TOS,
		'HOST_UNREACHABLE_FOR_TOS':              HOST_UNREACHABLE_FOR_TOS,
		'COMMUNICATION_PROHIBITED_BY_FILTERING': COMMUNICATION_PROHIBITED_BY_FILTERING,
		'HOST_PRECEDENCE_VIOLATION':             HOST_PRECEDENCE_VIOLATION,
		'PRECEDENCE_CUTOFF_IN_EFFECT':           PRECEDENCE_CUTOFF_IN_EFFECT,
		'REDIRECT_FOR_NETWORK':                  REDIRECT_FOR_NETWORK,
		'REDIRECT_FOR_HOST':                     REDIRECT_FOR_HOST,
		'REDIRECT_FOR_TOS_AND_NET':              REDIRECT_FOR_TOS_AND_NET,
		'REDIRECT_FOR_TOS_AND_HOST':             REDIRECT_FOR_TOS_AND_HOST,
		'TTL_EQ_ZERO_DURING_TRANSIT':            TTL_EQ_ZERO_DURING_TRANSIT,
		'TTL_EQ_ZERO_DURING_REASSEMBLY':         TTL_EQ_ZERO_DURING_REASSEMBLY,
		'REQUIRED_OPTION_MISSING':               REQUIRED_OPTION_MISSING,
		'IP_HEADER_BAD':                         IP_HEADER_BAD,
	}.items())

	# names would have non-unique keys

	def __str__ (self):
		return '%d' % int(self)
