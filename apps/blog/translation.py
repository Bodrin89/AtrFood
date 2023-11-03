from modeltranslation.translator import TranslationOptions, register

from apps.blog.models import Blog


@register(Blog)
class BlogTranslation(TranslationOptions):
    fields = ('theme', 'text')
