import unittest

# ------------
# 샘플 이벤트 모음
# ------------

DDBNew = {
    'Records' : [ {
        'eventID' : 'b2c856e01875070d343c9e7357370957', 'eventName' : 'MODIFY',
        'eventVersion' : '1.1', 'eventSource' : 'aws:dynamodb', 'awsRegion' : 'ap-northeast-2',
        'dynamodb' : {
            'ApproximateCreationDateTime' : 1494489900.0,
            'Keys' : { 'CastUid' : { 'S' : '35g7658cgcba27276233f69553815b' } },
            'NewImage' : {
                'Status' : { 'S' : 'end' }, 'CastTitle' : { 'S' : 'asdf' },
                'CastUid' : { 'S' : '35g7658cgcba27276233f69553815b' },
                'EndTime' : { 'S' : '2017-05-11T08:05:53.943061+0000' },
                'UserId' : { 'S' : '123' },
                'CreateTime' : { 'S' : '2017-05-11T07:17:27.149697+0000' },
                'StartTime' : { 'S' : '2017-05-11T07:19:18.263346+0000' }
            },
            'SequenceNumber' : '0', 'SizeBytes' : 224,
            'StreamViewType' : 'NEW_IMAGE'
        },
        'eventSourceARN' : 'arn'
    } ]
}


class MyTestCase( unittest.TestCase ) :
    def test_something( self ) :
        self.assertEqual( True, False )


if __name__ == '__main__' :
    unittest.main()
