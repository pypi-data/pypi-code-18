# coding: utf-8
from rest_framework.reverse import reverse
from .choices import (
    QUESTION_TYPE_RADIO,
    QUESTION_TYPE_SELECT,
    QUESTION_TYPE_CHECKBOXES,
)


def reverse_list(request, view_name, field, obj):

    """
    reverses a list name
    """
    return reverse(view_name, request=request) + '?{0}={1}'.format(field, obj)


def build_survey_data(survey):
    """
    From a survey, build survey
    data.

    survey_data is a dict with all
    the options, ready for rendering
    """
    return {
        'schema': build_schema(survey),
        'fieldsets': build_fieldsets(survey)
    }


def build_answer(answer):

    return {build_question_name(answer.question): answer.value}


def build_answers(surveyed):

    answer_data = {}
    for a in surveyed.answers:
        answer_data.update(build_answer(a))
    return answer_data


def get_question_by_name(question_name):

    from .models import Question
    if question_name.startswith('q'):
        return Question.objects.get(id=int(question_name[1:]))

    return None


def build_question_name(question):

    return 'q' + str(question.id)


def build_question(question):
    question_data = {}
    question_name = build_question_name(question)
    question_data[question_name] = {
        'name': question_name,
        'title': question.text,
        'help': question.help,
        'type': question.type
    }
    if question.type in (QUESTION_TYPE_RADIO,
                         QUESTION_TYPE_SELECT,
                         QUESTION_TYPE_CHECKBOXES):
        question_data[question_name]['options'] = question.options
        if question.other_token:
            question_name[question_name]['options'].append(question.other_token)

    if question.validators:
        question_data[question_name]['validators'] = question.validators

    if question.parent:
        question_data[question_name]['parent'] = build_question_name(question.parent)
        question_data[question_name]['parent_value'] = question.parent_value

    return question_data


def build_schema(survey):
    schema = {}
    questions = survey.questions.all()
    for q in questions:
        schema.update(build_question(q))
    return schema


def build_fieldsets(survey):

    sections = survey.sections.all()
    return [{s.title: [build_question_name(q) for q in s.questions.all()]} for s in sections]