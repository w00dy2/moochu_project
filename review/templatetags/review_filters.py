
from django import template

register = template.Library()

@register.filter
def remove_after_parenthesis(value):
    index = value.find('(')
    return value[:index] if index != -1 else value

@register.filter
def format_slash(value):
    return value.replace('/', '/<br>')