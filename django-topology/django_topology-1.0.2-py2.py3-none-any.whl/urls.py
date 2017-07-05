# coding: utf-8
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from topology.viewsets import (
    RuleViewSet,
    TopologyRuleViewSet,
    TopologyErrorViewSet,
)
from topology.views import TopologyCheckView


router = DefaultRouter(trailing_slash=False)
router.register('rules', RuleViewSet)
router.register('topology-rules', TopologyRuleViewSet)
router.register('topology-errors', TopologyErrorViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(
        r'^api/topology/check/$',
        TopologyCheckView.as_view(),
        name='topology-check'
    )
]
