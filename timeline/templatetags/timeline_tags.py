# -*- coding: utf-8 -*-
from django import template

# template library 등록
register = template.Library()


# record set 'target_rs' 에 'item' 이 존재하는지
@register.filter(name='has')
def has(target_rs, item):
    if (item == None): return False
    if (target_rs.filter(id=item.id).exists()): return True
    return False
    