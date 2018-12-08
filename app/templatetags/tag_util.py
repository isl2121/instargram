from django import template
from ..models import Tag
from django.urls import reverse
import re

register = template.Library()

@register.filter
def tag_link(val):
    content = val.content

    for tags in val.tag_setting.all():
        content = re.sub(r'\#'+tags.tag+r'\b', "<a href='"+reverse('app:get_tag', kwargs={'tag':tags.tag})+"'>#"+tags.tag+"</a>", content)
    return content

#