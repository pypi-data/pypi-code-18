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


class SurveyViewSet(DefaultViewSetMixIn,
                    ModelViewSet):

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SectionViewSet(DefaultViewSetMixIn,
                     ModelViewSet):

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class QuestionViewSet(DefaultViewSetMixIn,
                      ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SurveyedObjectViewSet(DefaultViewSetMixIn,
                            ModelViewSet):

    queryset = SurveyedObject.objects.all()
    serializer_class = SurveyedObjectSerializer


class AnswerViewSet(DefaultViewSetMixIn,
                    ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class OtherAnswerViewSet(DefaultViewSetMixIn,
                         ModelViewSet):

    queryset = OtherAnswer.objects.all()
    serializer_class = OtherAnswerSerializer
