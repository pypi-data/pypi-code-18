'''
Created on Sep 18, 2016

@author: sridharn
'''
import json
import requests
import hashlib
import logging

class VoiceInsights:
    
    appToken = ''
    sessionId = None

        
    def sendVLEvent(self, payload):
        url = "https://api.voicelabs.co/events"
        params = { "auth_token" : payload['app_token'], "sdk" : "assistant_python-1.0.0"}
        data_json = json.dumps(payload)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, params=params, data=data_json, headers=headers, timeout=1)
        return response


    def md5(self, input_string):
        return hashlib.md5(input_string).hexdigest()
        
            
    def __init__(self, appToken):
        try:

            if appToken is None or len(appToken.strip()) == 0 or not isinstance(appToken, basestring):
                logging.error("ERROR: cannot initialize VoiceInsights SDK. either session or appToken are 'None'")
                return

            self.appToken = appToken

            return None

        except Exception as err:
            print err
            logging.error("ERROR: occurred inside initalize")
            return None
        

    def track(self, intentName, request, agentTTS):
    
        try:    
            
            conversation_id = None
            user_id = None
            
            #Error check to make sure we have everything we need
            if self.appToken is None or len(self.appToken.strip()) == 0 or not isinstance(self.appToken, basestring):
                logging.error("ERROR: Voicelabs SDK wasn't initialized properly. Found an invalid appToken")
                return

            if not request or not type(request) is dict:
                logging.error("ERROR: Voicelabs SDK was passed an Invalid request object")
                return
            
             #Supporting non-back comp V1 and V2 Google APIs
            if request.get('conversation',{}).has_key('conversation_id'):
                conversation_id = request['conversation']['conversation_id']
            elif request.get('conversation',{}).has_key('conversationId'):
                conversation_id = request['conversation']['conversationId']
                
            if request.get('user',{}).has_key('user_id'):
                user_id = request['user']['user_id']
            elif request.get('user',{}).has_key('userId'):
                user_id = request['user']['userId']

            if not conversation_id:
                logging.error("ERROR: Invalid conversation object passed through request.")
                return

            if not user_id:
                logging.error("ERROR: Invalid user object passed through request.")
                return
            
            if not intentName or len(intentName.strip()) == 0 or not isinstance(intentName, basestring):
                logging.error("ERROR: Invalid intentName was passed to track")
                return 

            p =  {}
            p['app_token'] = self.appToken
            p['user_hashed_id'] = self.md5(user_id)
            p['session_id'] = conversation_id
            
            if not self.sessionId or self.sessionId != conversation_id:
                #found new session, so fire an initialize event
                p['event_type'] = 'INITIALIZE'
                p['intent'] = intentName
                p['data'] = None
                self.sessionId = conversation_id
                resp = self.sendVLEvent(p)

            #now send the track event
            userSpeech = None
            if isinstance(request.get('inputs',{}), list) and isinstance(request.get('inputs')[0].get('rawInputs',{}), list ) > 0 and request.get('inputs')[0].get('rawInputs')[0].has_key('query'):
                userSpeech = request['inputs'][0]['rawInputs'][0]['query']

            p['event_type'] = 'SPEECH'
            p['intent'] = intentName
            p['data'] = {}
            p['data']['metadata'] = userSpeech
            p['data']['speech'] = agentTTS

            resp = self.sendVLEvent(p)             
            return resp

        except Exception as err:
            print err
            logging.error("ERROR: occurred inside track method")
            return None
    