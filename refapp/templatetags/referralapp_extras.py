from django import template
import datetime

register = template.Library()

@register.filter(name='epoch_datetime')
def epoch_datetime(value):
    return datetime.datetime.fromtimestamp(int(value))