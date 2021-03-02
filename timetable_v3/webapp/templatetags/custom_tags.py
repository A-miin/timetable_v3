from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    n, start = int(number), 0
    if number > 1:
        start = n*5-5
    return range(start, n*5)


@register.filter
def index(indexable, i):
    if type(i) == str:
        return indexable.i
    else:
        return indexable[i]

@register.filter
def get_type(type_code):
    types = {
        0: 'success',
        1: 'primary',
        2: 'warning',
        3: 'secondary',
        5: 'secondary'
    }
    return types[type_code]
