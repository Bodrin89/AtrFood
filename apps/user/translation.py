from modeltranslation.translator import TranslationOptions, register
from apps.user.models import BaseUserModel
from apps.clients.models import AddressModel


@register(AddressModel)
class AddressTranslationOptions(TranslationOptions):
    fields = ('district', 'street')
