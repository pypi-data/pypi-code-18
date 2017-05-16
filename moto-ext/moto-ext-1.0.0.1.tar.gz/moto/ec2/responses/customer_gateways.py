from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from moto.ec2.utils import filters_from_querystring


class CustomerGateways(BaseResponse):

    def create_customer_gateway(self):
        # raise NotImplementedError('CustomerGateways(AmazonVPC).create_customer_gateway is not yet implemented')
        type = self.querystring.get('Type', None)[0]
        ip_address = self.querystring.get('IpAddress', None)[0]
        bgp_asn = self.querystring.get('BgpAsn', None)[0]
        customer_gateway = self.ec2_backend.create_customer_gateway(
            type, ip_address=ip_address, bgp_asn=bgp_asn)
        template = self.response_template(CREATE_CUSTOMER_GATEWAY_RESPONSE)
        return template.render(customer_gateway=customer_gateway)

    def delete_customer_gateway(self):
        customer_gateway_id = self.querystring.get('CustomerGatewayId')[0]
        delete_status = self.ec2_backend.delete_customer_gateway(
            customer_gateway_id)
        template = self.response_template(DELETE_CUSTOMER_GATEWAY_RESPONSE)
        return template.render(customer_gateway=delete_status)

    def describe_customer_gateways(self):
        filters = filters_from_querystring(self.querystring)
        customer_gateways = self.ec2_backend.get_all_customer_gateways(filters)
        template = self.response_template(DESCRIBE_CUSTOMER_GATEWAYS_RESPONSE)
        return template.render(customer_gateways=customer_gateways)


CREATE_CUSTOMER_GATEWAY_RESPONSE = """
<CreateCustomerGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <customerGateway>
      <customerGatewayId>{{ customer_gateway.id }}</customerGatewayId>
      <state>pending</state>
      <type>{{ customer_gateway.type }}</type>
      <ipAddress>{{ customer_gateway.ip_address }}</ipAddress>
      <bgpAsn>{{ customer_gateway.bgp_asn }}</bgpAsn>
    <tagSet>
      {% for tag in customer_gateway.get_tags() %}
        <item>
          <resourceId>{{ tag.resource_id }}</resourceId>
          <resourceType>{{ tag.resource_type }}</resourceType>
          <key>{{ tag.key }}</key>
          <value>{{ tag.value }}</value>
        </item>
      {% endfor %}
    </tagSet>
   </customerGateway>
</CreateCustomerGatewayResponse>"""

DELETE_CUSTOMER_GATEWAY_RESPONSE = """
<DeleteCustomerGatewayResponse xmlns="http://ec2.amazonaws.com/doc/2013-10-15/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <return>{{ delete_status }}</return>
</DeleteCustomerGatewayResponse>"""

DESCRIBE_CUSTOMER_GATEWAYS_RESPONSE = """
<DescribeCustomerGatewaysResponse xmlns="http://ec2.amazonaws.com/doc/2014-10- 01/">
  <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
  <customerGatewaySet>
  {% for customer_gateway in customer_gateways %}
    <item>
       <customerGatewayId>{{ customer_gateway.id }}</customerGatewayId>
       <state>{{ customer_gateway.state }}</state>
       <type>available</type>
       <ipAddress>{{ customer_gateway.ip_address }}</ipAddress>
       <bgpAsn>{{ customer_gateway.bgp_asn }}</bgpAsn>
    <tagSet>
      {% for tag in customer_gateway.get_tags() %}
        <item>
          <resourceId>{{ tag.resource_id }}</resourceId>
          <resourceType>{{ tag.resource_type }}</resourceType>
          <key>{{ tag.key }}</key>
          <value>{{ tag.value }}</value>
        </item>
      {% endfor %}
    </tagSet>
    </item>
  {% endfor %}
  </customerGatewaySet>
</DescribeCustomerGatewaysResponse>"""
