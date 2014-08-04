# -*- coding: utf-8 -*-
"""
Markup tags
"""
from django import template
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def text_transform(content):
    # TODO: to be or not to be ?
    return content
