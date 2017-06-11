# -*- coding: utf-8 -*-
"""
Request sample
{
  "messageVersion": "1.0",
  "invocationSource": "FulfillmentCodeHook or DialogCodeHook",
  "userId": "user-id specified in the POST request to Amazon Lex.",
  "sessionAttributes": { 
     "key1": "value1",
     "key2": "value2",
  },
  "bot": {
    "name": "bot-name",
    "alias": "bot-alias",
    "version": "bot-version"
  },
  "outputDialogMode": "Text or Voice, based on ContentType request header in runtime API request",
  "currentIntent": {
    "name": "intent-name",
    "slots": {
      "slot-name": "value",
      "slot-name": "value",
      "slot-name": "value"
    },
    "confirmationStatus": "None, Confirmed, or Denied (intent confirmation, if configured)"
  }
}

Response sample

{
  "sessionAttributes": {
    "key1": "value1",
    "key2": "value2"
    ...
  },
  "dialogAction": {
    "type": "ElicitIntent, ElicitSlot, ConfirmIntent, Delegate, or Close",
    "fulfillmentState": "Fulfilled or Failed",
    "message": {
      "contentType": "PlainText or SSML",
      "content": "message to convey to the user"
    },
   "intentName": "intent-name",
   "slots": {
      "slot-name": "value",
      "slot-name": "value",
      "slot-name": "value"  
   },
   "slotToElicit" : "slot-name",
   "responseCard": {
      "version": integer-value,
      "contentType": "application/vnd.amazonaws.card.generic",
      "genericAttachments": "[
          {
             "title":"card-title",
             "subTitle":"card-sub-title",
             "imageUrl":"URL of the image to be shown",
             "attachmentLinkUrl":"URL of the attachment to be associated with the card",
             "buttons":[ 
                 {
                    "text":"button-text",
                    "value":"value sent to server on button click"
                 }
              ]
           } 
       ]"  
     }
  }
}
"""

class Request(object):

    def __init__(self, dic):
        self.content = dic

    def to_dict(self):
        self.content['sessionAttributes'] = json.loads(self.content['sessionAttributes'])
        return dict(self.content)


class Response(object):

    def __init__(self, dic):
        self.content = dic

    def with_session_attributes(self, session_attributes):
        self.content['sessionAttributes'] = session_attributes
        return self

    def to_dict(self):
        return dict(self.content)

class ResponseBuilder(object):

    @classmethod
    def elicit_intent(self, message=None, card=None):
        '''
            Argments

            #Optional

            message:
                Optional. you can build message using MessageBuilder.
                If message is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)

            card:
                Optional. you can build card using CardBuilder.
                If card is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)
        '''
        response = self._build_response('ElicitIntent', message=message, card=card)
        return Response(response)

    @classmethod
    def elicit_slot(self, intent_name, slot_to_elicit, slots, message=None, card=None):
        '''
            Argments

            # Required

            intent_name:
                Basicaly, set requests['currentIntent']['name']

            slots:
                Slots must include all of the slots configured for the intent.
                If the value of a slot is unknown, it must be explicitly set to null (similar to Lambda function request)

            slot_to_elicit:
                 Informs Amazon Lex that the user is expected to provide a slot value in response.
                 For example, a value for the pizzaSize or pizzaKind slots.

            # Optional

            message:
                Optional. you can build message using MessageBuilder.
                If message is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)

            card:
                Optional. you can build card using CardBuilder.
                If card is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)
        '''
        response = self._build_response('ElicitSlot', intent_name=intent_name, slot_to_elicit=slot_to_elicit, slots=slots, message=message, card=card)
        return Response(response)

    @classmethod
    def confirm_intent(self, intent_name, slots, message=None, card=None):
        '''
            Argments

            # Required

            intent_name:
                Basicaly, set requests['currentIntent']['name']

            slots:
                Slots must include all of the slots configured for the intent.
                If the value of a slot is unknown, it must be explicitly set to null (similar to Lambda function request)

            # Optional

            message:
                You can build message using MessageBuilder.
                If message is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)

            card:
                You can build card using CardBuilder.
                If card is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)
        '''
        response = self._build_response('ConfirmIntent', intent_name=intent_name, slots=slots, message=message, card=card)
        return Response(response)

    @classmethod
    def delegate(self, slots):
        '''
            Argments

            # Required

            slots:
                Slots must include all of the slots configured for the intent.
                If the value of a slot is unknown, it must be explicitly set to null (similar to Lambda function request)
        '''
        response = self._build_response('Delegate', slots=slots)
        return Response(response)

    @classmethod
    def close(self, fulfillment_state, message=None, card=None):
        '''
            Argments

            # Required

            fulfillment_state:
                Set 'Fulfilled' or 'Failed'.
                Amazon Lex uses this value to set the dialogState in its response to the client.

            # Optional

            message:
                You can build message using MessageBuilder.
                If message is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)

            card:
                You can build card using CardBuilder.
                If card is None, Amazon Lex uses one of the bot's
                clarification prompts.(see the Error Handling section in the console.)
        '''
        response = self._build_response('Close', fulfillment_state=fulfillment_state, message=message, card=card)
        return Response(response)

    @classmethod
    def _build_response(self, response_type, fulfillment_state=None, message=None, intent_name=None, slots=None, slot_to_elicit=None, card=None):

        dic = {
                'dialogAction': {
                        'type': response_type,
                    }
                }

        if fulfillment_state:
            dic['dialogAction']['fulfillmentState'] = fulfillment_state

        if message:
            dic['dialogAction']['message'] = message

        if card:
            dic['dialogAction']['responseCard'] = card

        if intent_name:
            dic['dialogAction']['intentName'] = intent_name

        if slots:
            dic['dialogAction']['slots'] = slots

        if slot_to_elicit:
            dic['dialogAction']['slotToElicit'] = slot_to_elicit

        return dic

class Card(object):
    def __init__(self, dic):
        self.content = dic

    def with_buttons(self, buttons):
        self.content['genericAttachments']['buttons'] = buttons
        return self

    def to_dict(self):
        return dict(self.content)

class CardBuilder(object):

    @classmethod
    def build_response_card(version=None, title=None, sub_title=None, image_url=None, attachment_link_url=None):
        '''
            See http://docs.aws.amazon.com/ja_jp/lex/latest/dg/ex-resp-card.html
        '''
        card_contents = {
                'contentType': 'application/vnd.amazonaws.card.generic'
                }
        generic_attachments = {}

        if version:
            card_contents['version'] = version
        if title:
            generic_attachments['title'] = title
        if sub_title:
            generic_attachments['subTitle'] = sub_title
        if image_url:
            generic_attachments['imageUrl'] = image_url
        if attachment_link_url:
            generic_attachments['attachmentLinkUrl'] = attachment_link_url

        card_contents['genericAttachments'] = generic_attachments

        return Card(card_contents)

class MessageBuilder(object):

    @classmethod
    def build_message(self, content, content_type="PlainText"):
        return {
                'contentType': content_type,
                'content': content
                }
