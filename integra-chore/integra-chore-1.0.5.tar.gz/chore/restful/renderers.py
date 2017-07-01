from rest_framework.renderers import JSONRenderer

class CsvRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'element': data}
        return super(EmberJSONRenderer, self).render(data, accepted_media_type, renderer_context)