# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .validation import TopologyChecker
from .serializers import (
    TopologyErrorSerializer,
)


class TopologyCheckView(APIView):

    def process_arguments(self, request):
        content_type_id = request.data.get('content_type_id', None)
        feature_id = request.data.get('feature_id', None)
        rules = request.data.get('rules', None)
        persist = request.data.get('persist', False)

        if not content_type_id:
            raise ValidationError('content_type_id is mandatory')

        if not rules:
            rules = '__all__'

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise ValidationError('content_type with id %s does not exists' % content_type_id)

        model = content_type.model_class()

        if feature_id:
            qs = model.objects.filter(pk=feature_id)
        else:
            qs = model.objects.all()

        return {
            'rules': rules,
            'model': model,
            'content_type': content_type,
            'queryset': qs,
            'persist': persist
        }

    def process_request(self, request):
        """
        Core function. all the action happens here.
        Gets the data from the request, extracts useful
        info and feed that into the TopoChecker.
        Returns errors.
        Persist is optional.
        """
        data = self.process_arguments(request)
        queryset = data.get('queryset')
        rules = data.get('rules')
        persist = data.get('persist')
        topo_checker = TopologyChecker(persist=persist)
        errors = topo_checker.validate(queryset, rules)
        serializer = TopologyErrorSerializer(errors, many=True)
        return Response(serializer.data)

    def post(self, request, format='json'):
        """
        checks errors and
        persists them into the database
        """
        return self.process_request(request)
