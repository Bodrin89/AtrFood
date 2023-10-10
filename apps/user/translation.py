

from modeltranslation.translator import TranslationOptions, register

from apps.user.models import BaseUserModel, RegionModel, AddressModel


@register(RegionModel)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region', 'city')


@register(BaseUserModel)
class BaseUserTranslationOptions(TranslationOptions):
    fields = ('region',)


@register(AddressModel)
class AddressTranslationOptions(TranslationOptions):
    fields = ('district', 'street')