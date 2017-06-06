import re
import boto3

from django.conf import settings

from base.exceptions import DoesNotExist
from fields import AVAILABLE_FIELDS, AVAILABLE_KEY_FIELDS


# Get the service resource.
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def _camelcase_to_underscore(name):
    """
    A method used for converting Camelcase class name to Underscore format string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Table(object):
    """
    A base Table class for implementing the basic components of a Dynamo DB.
    """
    TABLE_NAME = None
    KEY_FIELDS = {}
    FIELDS = {}
    KEY_DATA = {}
    DATA = {}

    def _extract_fields(self):
        """
        Extracts all the Field objects from other attributes.
        """
        attrs = type(self).__dict__
        for attr in attrs.keys():
            # Add attribute if it is a Key Field object
            if type(attrs[attr]).__name__ in AVAILABLE_KEY_FIELDS:
                self.KEY_FIELDS[attr] = attrs[attr]
                continue
            # Add attribute if it is a Field object
            if type(attrs[attr]).__name__ in AVAILABLE_FIELDS:
                self.FIELDS[attr] = attrs[attr]

    def _validate_input(self, data):
        """
        Check if initializer data keys belong to the Fields.
        Save value in DATA dict if it is among the Fields, else raise error.
        """
        for key in data.keys():
            if key not in self.KEY_FIELDS.keys() and key not in self.FIELDS.keys():
                raise ValueError('The field %s is not defined' % key)
            self.__setattr__(key, data[key])

    def __init__(self, *args, **kwargs):
        self.TABLE_NAME = _camelcase_to_underscore(type(self).__name__)
        self._extract_fields()
        if kwargs:
            self._validate_input(kwargs)

    def __getattr__(self, key):
        super(Table, self).__setattr__(key)

    def __setattr__(self, key, value):
        """
        Save value in DATA dict if it is among the Fields.
        """
        if key in self.KEY_FIELDS.keys():
            self.KEY_DATA[key] = value
        if key in self.FIELDS.keys():
            self.DATA[key] = value
        super(Table, self).__setattr__(key, value)

    def _create_key_schema(self):
        """
        Creates KeySchema dict necessary while creating the Database.
        It defines the Hash and Range keys.
        """
        key_schema = []
        for field_name in self.KEY_FIELDS.keys():
            field = self.KEY_FIELDS[field_name]
            # Detect and attach HashKeyField in the KeySchema
            if type(field).__name__ == 'HashKeyField':
                key_schema.append({
                    'AttributeName': field_name,
                    'KeyType': 'HASH'})
            # Detect and attach RangeKeyField in the KeySchema
            if type(self.KEY_FIELDS[field_name]).__name__ == 'RangeKeyField':
                key_schema.append({
                    'AttributeName': field_name,
                    'KeyType': 'RANGE'})
        if len(key_schema) == 0:
            raise ValueError('Model must have one HashKeyField')
        return key_schema

    def _create_attribute_definitions(self):
        """
        Creates AttributeDefinitions dict necessary while creating the Database.
        It defines the Hash and Range keys.
        """
        attribute_definitions = []
        for field_name in self.KEY_FIELDS.keys():
            field = self.KEY_FIELDS[field_name]
            # Detect and attach HashKeyField in the AttributeDefinitions
            if type(field).__name__ == 'HashKeyField':
                attribute_definitions.append({
                    'AttributeName': field_name,
                    'AttributeType': field.ATTRIBUTE_TYPE})
            # Detect and attach RangeKeyField in the AttributeDefinitions
            if type(self.KEY_FIELDS[field_name]).__name__ == 'RangeKeyField':
                attribute_definitions.append({
                    'AttributeName': field_name,
                    'AttributeType': field.ATTRIBUTE_TYPE})
        if len(attribute_definitions) == 0:
            raise ValueError('Model must have one HashKeyField')
        return attribute_definitions

    def _create_table(self):
        """
        Creates the actual table in DynamoDB.
        """
        key_schema = self._create_key_schema()
        attribute_definitions = self._create_attribute_definitions()

        table = dynamodb.create_table(
            TableName=self.TABLE_NAME,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            })

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=self.TABLE_NAME)
        return True

    def _if_table_exists(self):
        """
        Checks if the table exists yet or not
        """
        try:
            table = dynamodb.Table(self.TABLE_NAME)
            table.creation_date_time
            return True
        except Exception:
            return False

    @classmethod
    def get(cls, *args, **kwargs):
        """
        Gets model data from Dynamo DB
        """
        table = dynamodb.Table(_camelcase_to_underscore(cls.__name__))
        response = table.get_item(
            Key=kwargs)
        try:
            data = response['Item']
        except KeyError:
            raise DoesNotExist('The \'%s\' item does not exist' % cls.__name__)
        # Create a populated instance of the Table which called get()
        return cls(**data)

    def save(self):
        """
        Saves model data to Dynamo DB
        """
        table = dynamodb.Table(self.TABLE_NAME)
        # Merge keys and other fields
        data = dict(self.KEY_DATA, **self.DATA)
        table.put_item(
            Item=data)
        return True

    def update(self):
        """
        Saves model data to Dynamo DB
        """
        table = dynamodb.Table(self.TABLE_NAME)

        update_expression = ','.join('%s=:%s' % (key, key) for key in self.DATA.keys())
        update_expression = 'set %s' % update_expression
        expression_attr_vals = {':%s' % key: self.DATA[key] for key in self.DATA.keys()}

        response = table.update_item(
            Key=self.KEY_DATA,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attr_vals,
            ReturnValues='UPDATED_NEW')
        return response

    def delete(self):
        """
        Deletes model data from Dynamo DB
        """
        table = dynamodb.Table(self.TABLE_NAME)
        table.delete_item(
            Key=self.KEY_DATA)
        return True
