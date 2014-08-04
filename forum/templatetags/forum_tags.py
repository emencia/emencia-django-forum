# -*- coding: utf-8 -*-
"""
Common tags
"""
import datetime

from django.conf import settings
from django import template
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

from forum.models import Thread

register = template.Library()

@register.inclusion_tag('forum/thread_widget_announces.html', takes_context=True)
def display_announces(context):
    _delta_now = datetime.datetime.today() + datetime.timedelta(weeks=-2)
    
    announces_queryset = Thread.objects.filter(category__visible=True, visible=True, announce=True, created__gte=_delta_now).order_by('-modified')
    
    return {
        'user': context['user'],
        'announces': announces_queryset,
    }
