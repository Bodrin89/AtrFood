from modeltranslation.translator import TranslationOptions, register
from apps.company_user.models import CompanyUserModel, ContactPersonModel


@register(ContactPersonModel)
class ContactPersonTranslationOptions(TranslationOptions):
    fields = ('surname', 'first_name', 'second_name')


@register(CompanyUserModel)
class CompanyUserTranslationOptions(TranslationOptions):
    # fields = ('contact_person', )
    pass
