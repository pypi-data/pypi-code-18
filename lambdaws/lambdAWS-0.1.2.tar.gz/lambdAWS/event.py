"""
get AWS lambda input event data
"""

from .record import DDBStream, S3Sns, Sns, S3

EventResource = {
            "dynamodb" : DDBStream,
            "s3" : S3,
            "sns" : Sns,
            "s3sns" : S3Sns,
        }

class LambdaEvent :
    """
    이벤트로 들어오는 메시지를 레코드 객체로 변환 및 다중 레코드를 처리함
    """

    def __init__( self, event, source ) :


        self._RawEvent = event
        self.__ResourceClass = EventResource[ source ]

        # 이벤트 소스 목록


        self._RawRecords = self._RawEvent[ 'Records' ]
        # 레코드 갯수
        self.count = len( self._RawRecords )
        self._RawRecord = self._RawRecords[ 0 ] if self.count == 1 else None

        self._record = None

    @property
    def record( self ) :
        if self._record == None :
            self._record = self.__ResourceClass(self._RawRecord)
        return self._record
