class JSONSuitMixin(object):
    jsonsuit_fields = ()

    def get_readonly_fields(self, request, obj=None):
        ro_fields = super(JSONSuitMixin, self).get_readonly_fields(request, obj)
        for field in set(ro_fields).intersection(jsonsuit_fields):
            field.widget = None
