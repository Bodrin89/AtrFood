from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from apps.promotion.tasks import send_email_promotion
from apps.promotion.models import DiscountModel, LoyaltyModel
from config.settings import LOGGER

def resend_promotion_email(modeladmin, request, queryset):
    """Добавление действия отправки повторного email с акцией"""
    for discount in queryset:
        LOGGER.debug(discount.name)
        send_email_promotion.apply_async(args=[discount.name])
    modeladmin.message_user(request, _('Emails resent successfully.'), messages.SUCCESS)

resend_promotion_email.short_description = _('Отправить email с акцией')

# def resend_promotion_email(modeladmin, request, queryset):
#     """Добавление действия отправки повторного email с акцией"""
#     for discount in queryset:
#         LOGGER.debug(discount.name)
#         send_email_promotion.delay()
#     modeladmin.message_user(request, _('Emails resent successfully.'), messages.SUCCESS)
#
#
# resend_promotion_email.short_description = _('Отправить email с акцией')

@admin.register(DiscountModel)
class DiscountModelAdmin(admin.ModelAdmin):
    actions = [resend_promotion_email]


@admin.register(LoyaltyModel)
class LoyaltyAdmin(admin.ModelAdmin):
    pass
