# coding: utf-8
from rest_framework.viewsets import ModelViewSet
from common.viewsets import DefaultViewSetMixIn
from .models import (
    Survey,
    Section,
    Question,
    SurveyedObject,
    Answer,
    OtherAnswer,
)
from .serializers import (
    SurveySerializer,
    SectionSerializer,
    QuestionSerializer,
    SurveyedObjectSerializer,
    AnswerSerializer,
    OtherAnswerSerializer,
)
from .filters import (
    SurveyFilter,
    SectionFilter,
    QuestionFilter,
    AnswerFilter,
    OtherAnswerFilter,
    SurveyedObjectFilter,
)


class SurveyViewSet(DefaultViewSetMixIn,
                    ModelViewSet):

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_class = SurveyFilter
    search_fields = (
        'id',
        'name'
    )


class SectionViewSet(DefaultViewSetMixIn,
                     ModelViewSet):

    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_class = SectionFilter
    search_fields = (
        'id',
        'survey',
        'title',
    )


class QuestionViewSet(DefaultViewSetMixIn,
                      ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_class = QuestionFilter
    search_fields = (
        'id',
        'survey',
        'section',
        'type',
        'text',
    )


class SurveyedObjectViewSet(DefaultViewSetMixIn,
                            ModelViewSet):

    queryset = SurveyedObject.objects.all()
    serializer_class = SurveyedObjectSerializer
    filter_class = SurveyedObjectFilter
    search_fields = (
        'id',
        'survey',
    )


class AnswerViewSet(DefaultViewSetMixIn,
                    ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_class = AnswerFilter
    search_fields = (
        'id',
        'surveyed',
        'question',
    )


class OtherAnswerViewSet(DefaultViewSetMixIn,
                         ModelViewSet):

    queryset = OtherAnswer.objects.all()
    serializer_class = OtherAnswerSerializer
    filter_class = OtherAnswerFilter
    search_fields = (
        'id',
        'value'
    )
