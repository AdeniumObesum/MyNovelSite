#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mytags.py
# @Author: A.O.
# @Date  : 2018/6/3 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django import template

from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def render_page_ele(loop_counter, content_set):
    ele_class = ''
    if content_set.number == loop_counter:
        ele_class = "active"
    if loop_counter <= content_set.number:
        if loop_counter <= 3 or content_set.number - 4 < loop_counter:
            if loop_counter == 3 and content_set.number > 6:
                ele = '''<li><span>...</span></li>'''
            else:
                ele = '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (
                    ele_class,loop_counter,loop_counter)
            return mark_safe(ele)
    elif loop_counter > content_set.number:
        if loop_counter > content_set.paginator.num_pages - 3 or loop_counter < content_set.number + 4:
            if loop_counter == content_set.paginator.num_pages - 2 and content_set.paginator.num_pages - content_set.number > 5:
                ele = '''<li><span>...</span></li>'''
            else:
                ele = '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (
                    ele_class,loop_counter,loop_counter)
            return mark_safe(ele)
    # ele = '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (ele_class,loop_counter,loop_counter)
    # ele = '''<li><a>123</a></li>'''
    return ''