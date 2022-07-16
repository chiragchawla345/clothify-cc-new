from django import template

register = template.Library()


@register.filter(name='split_first')
def split_first(value, key):
    """
      Returns the value turned into a list.
    """
    return str(value).split(key)[0]


@register.filter(name='split_second')
def split_second(value, key):
    """
      Returns the value turned into a list.
    """
    return str(value).split(key)[1]
