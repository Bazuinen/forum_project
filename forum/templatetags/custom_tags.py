from django import template
from forum.models import Post  # moet correct zijn

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def get_latest_post_for_category(category):
    return Post.objects.filter(topic__category=category).order_by('-created_at').first()
