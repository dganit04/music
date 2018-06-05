from django import template

register = template.Library()
from random import randint
from string import capwords


# custom filter (upper) and assignment-tag (get-random)


@register.assignment_tag(name='get_random')
def get_random(*args, **kwargs):
    set = kwargs['songs']
    all_ids = set.values_list('id', flat=True)  # getting all songs based on one field, converting dict to flat list
    ran = all_ids[randint(0, len(all_ids) - 1)]
    item = set.filter(id=ran)
    print 'ran-id ', ran, item
    return ran


@register.filter
def upper(value):
    # returns capitalize of every word
    if value:
        return capwords(value)
    return value
