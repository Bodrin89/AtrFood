from modeltranslation.translator import TranslationOptions, register

from apps.library.models import AboutCompany, PrivacyPolicy, ReturnPolicy


@register(AboutCompany)
class AboutCompanyTranslation(TranslationOptions):
    """Перевод полей в модели AboutCompany"""
    fields = ('name',)


@register(PrivacyPolicy)
class PrivacyPolicyTranslation(TranslationOptions):
    """Перевод полей в модели PrivacyPolicy"""
    fields = ('name',)


@register(ReturnPolicy)
class ReturnPolicyTranslation(TranslationOptions):
    """Перевод полей в модели ReturnPolicy"""
    fields = ('name',)
