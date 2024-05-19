from django import template
from ..models import Like

register = template.Library()

@register.filter
def is_liked_by_user(post, user):
    return Like.objects.filter(post=post, user=user).exists()
