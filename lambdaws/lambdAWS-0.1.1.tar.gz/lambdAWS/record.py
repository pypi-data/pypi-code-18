from boto3.dynamodb.types import TypeDeserializer


class Record :
    def __init__( self, raw_record ) :
        self.raw = raw_record
        self.resource = self.raw[ 'eventSource' ][ 4 : ]
        self.region = self.raw[ 'awsRegion' ]
        self.eventID = self.raw[ 'eventID' ]
        try :
            self.eventName = self.raw[ 'eventName' ]
        except KeyError :
            pass
        self.get_item()

    def get_item( self ) :
        """
        이 메소드를 오버라이드하여 각 리소스에 맞는 정보를 추출한다 
        :return: 
        """
        pass


# DynamoDB Stream Event
class DDBStream( Record ) :
    """
    DynamoDB Stream Event를 통해 들어온 정보를 파이썬으로 직졀화합니다.
    Stream Event중 KEYS_ONLY,OLD_IMAGE,NewImage 이 3가지는 필드명으로 메소드 접근이 가능하다.
    ex) abc라는 필드 명이 있을 경우 DDBStream().abc 로 필드 값을 확인 가능함
    다만 NEW_AND_OLD_IMAGES일 경우 이전 값과 새로운 값을 모두 받아 들이기에 
    이전값을 self._old에 딕셔너리 형태로 저장함
    """
    def get_item( self ) :

        def deserialize( value ) :
            """
            boto3.dynamodb.types.TypeDeserializer을 이용하여 각 속성 값을 직렬화
            :param value: ddb field dict, ex) {"S":"foobar"}
            :return: 
            """
            return TypeDeserializer().deserialize( value )

        def get_attribute( dic: dict ) :
            """
            dict형식의 값을 파이썬 딕셔너리로 직렬화
            :param dic: 
            :return: 
            """
            attr = dic
            item = { }
            for key, value in attr, attr.items() :
                item[ 'key' ] = deserialize( value )
            return item

        raw = self.raw[ 'dynamodb' ]

        # 키값 직렬화
        keys = get_attribute( raw[ 'Keys' ] )
        self.__dict__.update( keys )

        # 스트림 종류에 따른 호출값 분기
        streamType = raw[ 'StreamViewType' ]

        if streamType == 'KEYS_ONLY' :
            pass
        elif streamType == 'NEW_IMAGE' :
            new = get_attribute( raw[ 'NewImage' ] )
            self.__dict__.update( new )
        elif streamType == 'OLD_IMAGE' :
            old = get_attribute( raw[ 'OldImage' ] )
            self.__dict__.update( old )
        elif streamType == 'NEW_AND_OLD_IMAGES' :
            new = get_attribute( raw[ 'NewImage' ] )
            old = get_attribute( raw[ 'OldImage' ] )
            self.__dict__.update( new )
            self.__dict__.update( { '_old' : old } )
        else :
            raise KeyError



# S3 Event
class S3( Record ) :
    pass


# Sns Event
class Sns( Record ) :
    pass


# S3 -> Sns Event
class S3Sns( Record ) :
    pass
