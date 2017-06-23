import json
from voicelabs import VoiceInsights

token = '97455a0a-a920-3d1b-abcb-36dba02c5141'

intentName = "TEST_INTENT"
agentTTS = "wasssaaaup!"
requestV1 = '{"user":{"user_id":"r6CbYTY+8MrzSgEWAi5yWtBGe0xU7Pn5KKEnlLK3YVo="},"conversation":{"conversation_id":"1484179642211","type":1},"inputs":[{"intent":"assistant.intent.action.MAIN","raw_inputs":[{"input_type":2,"query":"talk to silly name maker"}],"arguments":[]}]}'
requestV2 = '{"isInSandbox":true,"surface":{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]},"inputs":[{"rawInputs":[{"query":"Team","inputType":"TOUCH"}],"arguments":[{"rawText":"Team","textValue":"Team","name":"text"}],"intent":"actions.intent.TEXT"}],"user":{"locale":"en-US","userId":"APhe68HbF_lw38jyoPtDyB-XkKg1"},"device":{},"conversation":{"conversationId":"1498150330693","type":"ACTIVE"}}'

vi = VoiceInsights(token)
x = vi.track(intentName, json.loads(requestV1), agentTTS)
if x.json()['msg'] == 'success':
  print 'test case#1 passed'
else:
  print 'test case#1 failed'
  
x = vi.track(intentName, json.loads(requestV2), agentTTS)
if x and x.json()['msg'] == 'success':
  print 'test case#1V2 passed'
else:
  print 'test case#1V2 failed'

x = vi.track(None, None, None)
if x is None:
  print 'test case#2 passed'
else:
  print 'test case#2 failed'

x = vi.track(None, json.loads(requestV1), agentTTS)
if x is None:
  print 'test case#3 passed'
else:
  print 'test case#3 failed'

x = vi.track(None, json.loads(requestV2), agentTTS)
if x is None:
  print 'test case#3V2 passed'
else:
  print 'test case#3V2 failed'


x = vi.track(intentName, json.loads(requestV1), None)
if x.json()['msg'] == 'success':
  print 'test case#4 passed'
else:
  print 'test case#4 failed'
  
x = vi.track(intentName, json.loads(requestV2), None)
if x and x.json()['msg'] == 'success':
  print 'test case#4V2 passed'
else:
  print 'test case#4V2 failed'

x = vi.track(None, json.loads(requestV1), None)
if x is None:
  print 'test case#5 passed'
else:
  print 'test case#5 failed'
  
x = vi.track(None, json.loads(requestV2), None)
if x is None:
  print 'test case#5V2 passed'
else:
  print 'test case#5V2 failed'

#wihtout session_id
request = '{"user":{"user_id":"r6CbYTY+8MrzSgEWAi5yWtBGe0xU7Pn5KKEnlLK3YVo="},"conversation":{"type":1},"inputs":[{"intent":"assistant.intent.action.MAIN","raw_inputs":[{"input_type":2,"query":"talk to silly name maker"}],"arguments":[]}]}'
x = vi.track(intentName, json.loads(request), agentTTS)
if x is None:
  print 'test case#6 passed'
else:
  print 'test case#6 failed'

x = vi.track(intentName, "hello", agentTTS)
if x is None:
  print 'test case#7 passed'
else:
  print 'test case#7 failed'
