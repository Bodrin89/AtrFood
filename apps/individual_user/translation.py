

from modeltranslation.translator import TranslationOptions, register

from apps.individual_user.models import IndividualUserModel


@register(IndividualUserModel)
class BaseUserTranslationOptions(TranslationOptions):
    fields = ('second_phone_number', )
