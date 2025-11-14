# filepath: /home/lofa/DEV/lotfinitystudio/django/mysite/website/templatetags/custom_tags.py
from django import template
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ..models import InstagramPostSnippet

register = template.Library()

@register.simple_tag(takes_context=True)
def get_post_content(context, post_id):
    request = context['request']
    post = get_object_or_404(InstagramPostSnippet, id=post_id)
    return render_to_string("post_content.html", {"post": post, "request": request})