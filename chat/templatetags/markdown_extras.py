from django import template
from django.template.defaultfilters import stringfilter

from markdown2 import Markdown

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    markdowner = Markdown(extras=["fenced-code-blocks"])
    return markdowner.convert(value)