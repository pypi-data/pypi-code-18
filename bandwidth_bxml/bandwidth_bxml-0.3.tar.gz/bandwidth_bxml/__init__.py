import abc

from xml.etree.ElementTree import Element, tostring
import xml.dom.minidom


class Bxml(object):
    __metaclass__ = abc.ABCMeta
    root = None
    gender = "female"
    voice = "susan"
    locale = "en_US"
    nestable_verbs = ()

    def __init__(self, text=None, attrib=None, **kwargs):
        attrib = attrib or {}
        attrib.update(kwargs)
        attrib = {k: v for k, v in attrib.items() if v is not None}
        self.root = Element(self.classname, attrib=attrib)
        if text:
            self.root.text = text

    def append(self, element):
        assert not self.nestable_verbs or isinstance(element, self.nestable_verbs), "Cannot add {} verb to {}".format(
            element.classname, self.classname)
        root = element.root
        self.root.append(root)
        return element

    def to_string(self, pretty=False):
        response_str = '<?xml version="1.0" encoding="UTF-8"?>'
        response_str += tostring(self.root)
        # response_str = response_str.replace('requestURL', 'requestUrl')

        if pretty:
            xml_parsed = xml.dom.minidom.parseString(response_str)  # or xml.dom.minidom.parseString(xml_string)
            response_str = xml_parsed.toprettyxml()

        return response_str

    @property
    def classname(self):
        return self.__class__.__name__

    def speak(self, text, gender=None, voice=None, locale=None, **kwargs):
        """:rtype : SpeakSentence"""
        gender = gender or self.gender
        voice = voice or self.voice
        locale = locale or self.locale

        return self.append(SpeakSentence(text, gender, voice, locale=locale, **kwargs))

    def play(self, url, digits=None, **kwargs):
        """:rtype : PlayAudio"""
        return self.append(PlayAudio(url, digits=digits, **kwargs))

    def hangup(self):
        """:rtype : Hangup"""
        return self.append(Hangup())

    def record(self, requestUrl=None, requestUrlTimeout=None, fileFormat=None, terminatingDigits=None,
               maxDuration=None, transcribe=None, transcribeCallbackUrl=None, **kwargs):
        """:rtype : Record"""
        return self.append(Record(requestUrl=requestUrl,
                                  requestUrlTimeout=requestUrlTimeout,
                                  fileFormat=fileFormat,
                                  terminatingDigits=terminatingDigits,
                                  maxDuration=maxDuration,
                                  transcribe=transcribe,
                                  transcribeCallbackUrl=transcribeCallbackUrl,
                                  **kwargs))

    def transfer(self, transferTo, transferCallerId, callTimeout=None, requestUrl=None, requestUrlTimeout=None,
                 tag=None, **kwargs):
        """:rtype : Transfer"""
        return self.append(Transfer(transferTo=transferTo, transferCallerId=transferCallerId,
                                    callTimeout=callTimeout, requestUrl=requestUrl,
                                    requestUrlTimeout=requestUrlTimeout, tag=tag, **kwargs))

    def gather(self, requestUrl, requestUrlTimeout=None, terminatingDigits=None, maxDigits=None,
               interDigitTimeout=None, bargeable=None, **kwargs):
        """:rtype : Gather"""
        return self.append(Gather(requestUrl=requestUrl,
                                  requestUrlTimeout=requestUrlTimeout,
                                  terminatingDigits=terminatingDigits,
                                  maxDigits=maxDigits,
                                  interDigitTimeout=interDigitTimeout,
                                  bargeable=bargeable,
                                  **kwargs))

    def redirect(self, requestUrl, requestUrlTimeout, context=None, **kwargs):
        """:rtype : Redirect"""
        return self.append(
            Redirect(requestUrl=requestUrl, requestUrlTimeout=requestUrlTimeout, context=context, **kwargs))


class Response(Bxml):
    pass


class Pause(Bxml):
    def __init__(self, duration):
        super(Pause, self).__init__(duration=duration)


class SpeakSentence(Bxml):
    def __init__(self, text, gender=None, voice=None, locale=None, **kwargs):
        gender = gender or self.gender
        voice = voice or self.voice
        locale = locale or self.locale
        super(SpeakSentence, self).__init__(text=text, gender=gender, voice=voice, locale=locale, **kwargs)


class PlayAudio(Bxml):
    def __init__(self, url, digits=None, **kwargs):
        super(PlayAudio, self).__init__(text=url, digits=digits, **kwargs)


class Hangup(Bxml):
    pass


class PhoneNumber(Bxml):
    def __init__(self, phone_number):
        super(PhoneNumber, self).__init__(text=phone_number)


class Redirect(Bxml):
    def __init__(self, requestUrl, requestUrlTimeout, context=None, **kwargs):
        super(Redirect, self).__init__(requestUrl=requestUrl, requestUrlTimeout=requestUrlTimeout, context=context,
                                       **kwargs)


class Record(Bxml):
    def __init__(self, requestUrl=None, requestUrlTimeout=None, fileFormat=None, terminatingDigits=None,
                 maxDuration=None, transcribe=None, transcribeCallbackUrl=None, **kwargs):
        super(Record, self).__init__(requestUrl=requestUrl,
                                     requestUrlTimeout=requestUrlTimeout,
                                     fileFormat=fileFormat,
                                     terminatingDigits=terminatingDigits,
                                     maxDuration=maxDuration,
                                     transcribe=transcribe,
                                     transcribeCallbackUrl=transcribeCallbackUrl,
                                     **kwargs)


class Transfer(Bxml):
    nestable_verbs = (PlayAudio, SpeakSentence, Record, PhoneNumber)

    def __init__(self, transferTo, transferCallerId, callTimeout=None, requestUrl=None, requestUrlTimeout=None,
                 tag=None, **kwargs):
        if isinstance(transferTo, (list)):
            super(Transfer, self).__init__(transferCallerId=transferCallerId, callTimeout=callTimeout,
                                           requestUrl=requestUrl, requestUrlTimeout=requestUrlTimeout, tag=tag,
                                           **kwargs)
            for phone_number in transferTo:
                self.append(PhoneNumber(phone_number))
        else:
            super(Transfer, self).__init__(transferTo=transferTo, transferCallerId=transferCallerId,
                                           callTimeout=callTimeout, requestUrl=requestUrl,
                                           requestUrlTimeout=requestUrlTimeout, tag=tag, **kwargs)


class Gather(Bxml):
    nestable_verbs = (PlayAudio, SpeakSentence)

    def __init__(self, requestUrl, requestUrlTimeout=None, terminatingDigits=None, maxDigits=None,
                 interDigitTimeout=None, bargeable=None, **kwargs):
        super(Gather, self).__init__(requestUrl=requestUrl,
                                     requestUrlTimeout=requestUrlTimeout,
                                     terminatingDigits=terminatingDigits,
                                     maxDigits=maxDigits,
                                     interDigitTimeout=interDigitTimeout,
                                     bargeable=bargeable,
                                     **kwargs)
