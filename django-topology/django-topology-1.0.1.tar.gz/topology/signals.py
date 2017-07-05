# coding: utf-8
import django.dispatch

pre_check = django.dispatch.Signal(providing_args=['queryset', 'rules'])
post_check = django.dispatch.Signal(providing_args=['queryset', 'rules', 'errors'])
