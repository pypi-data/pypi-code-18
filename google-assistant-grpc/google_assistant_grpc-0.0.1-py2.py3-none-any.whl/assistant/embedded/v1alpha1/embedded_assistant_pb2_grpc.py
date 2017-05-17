# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import google.assistant.embedded.v1alpha1.embedded_assistant_pb2 as google_dot_assistant_dot_embedded_dot_v1alpha1_dot_embedded__assistant__pb2


class EmbeddedAssistantStub(object):
  """Service that implements Google Assistant API.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Converse = channel.stream_stream(
        '/google.assistant.embedded.v1alpha1.EmbeddedAssistant/Converse',
        request_serializer=google_dot_assistant_dot_embedded_dot_v1alpha1_dot_embedded__assistant__pb2.ConverseRequest.SerializeToString,
        response_deserializer=google_dot_assistant_dot_embedded_dot_v1alpha1_dot_embedded__assistant__pb2.ConverseResponse.FromString,
        )


class EmbeddedAssistantServicer(object):
  """Service that implements Google Assistant API.
  """

  def Converse(self, request_iterator, context):
    """Initiates or continues a conversation with the embedded assistant service.
    Each call performs one round-trip, sending an audio request to the service
    and receiving the audio response. Uses bidirectional streaming to receive
    results, such as the `END_OF_UTTERANCE` event, while sending audio.

    A conversation is one or more gRPC connections, each consisting of several
    streamed requests and responses.
    For example, the user says *Add to my shopping list* and the assistant
    responds *What do you want to add?*. The sequence of streamed requests and
    responses in the first gRPC message could be:

    *   ConverseRequest.config
    *   ConverseRequest.audio_in
    *   ConverseRequest.audio_in
    *   ConverseRequest.audio_in
    *   ConverseRequest.audio_in
    *   ConverseResponse.event_type.END_OF_UTTERANCE
    *   ConverseResponse.result.microphone_mode.DIALOG_FOLLOW_ON
    *   ConverseResponse.audio_out
    *   ConverseResponse.audio_out
    *   ConverseResponse.audio_out

    The user then says *bagels* and the assistant responds
    *OK, I've added bagels to your shopping list*. This is sent as another gRPC
    connection call to the `Converse` method, again with streamed requests and
    responses, such as:

    *   ConverseRequest.config
    *   ConverseRequest.audio_in
    *   ConverseRequest.audio_in
    *   ConverseRequest.audio_in
    *   ConverseResponse.event_type.END_OF_UTTERANCE
    *   ConverseResponse.result.microphone_mode.CLOSE_MICROPHONE
    *   ConverseResponse.audio_out
    *   ConverseResponse.audio_out
    *   ConverseResponse.audio_out
    *   ConverseResponse.audio_out

    Although the precise order of responses is not guaranteed, sequential
    ConverseResponse.audio_out messages will always contain sequential portions
    of audio.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_EmbeddedAssistantServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Converse': grpc.stream_stream_rpc_method_handler(
          servicer.Converse,
          request_deserializer=google_dot_assistant_dot_embedded_dot_v1alpha1_dot_embedded__assistant__pb2.ConverseRequest.FromString,
          response_serializer=google_dot_assistant_dot_embedded_dot_v1alpha1_dot_embedded__assistant__pb2.ConverseResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.assistant.embedded.v1alpha1.EmbeddedAssistant', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
