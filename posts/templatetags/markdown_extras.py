from django import template
from django.template.defaultfilters import stringfilter
from posts.models import Category,Author
import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.simple_tag
def get_categories():
    return Category.objects.all()[0:3]

@register.simple_tag
def get_authors():
    return Author.objects.all()[0:3]