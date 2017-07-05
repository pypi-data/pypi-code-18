# coding: utf-8
from rest_framework import viewsets
from .models import (
    Rule,
    TopologyRule,
    TopologyError,
)
from .serializers import (
    RuleSerializer,
    TopologyRuleSerializer,
    TopologyErrorSerializer,
)


class RuleViewSet(viewsets.ModelViewSet):

    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class TopologyRuleViewSet(viewsets.ModelViewSet):

    queryset = TopologyRule.objects.all()
    serializer_class = TopologyRuleSerializer


class TopologyErrorViewSet(viewsets.ModelViewSet):

    queryset = TopologyError.objects.all()
    serializer_class = TopologyErrorSerializer
