from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from apps.promotion.models import DiscountModel, LoyaltyModel
from apps.promotion.tasks import send_email_promotion
from config.settings import LOGGER
from django.contrib.auth import get_user_model

User = get_user_model()


def resend_promotion_email(modeladmin, request, queryset):
    """Добавление действия отправки повторного email с акцией"""

    users = User.objects.filter(is_active=True,  is_staff=False)
    emails = list(users.values_list('email', flat=True))
    for discount in queryset:
        send_email_promotion.apply_async(args=[discount.name, emails])
    modeladmin.message_user(request, _('Emails resent successfully.'), messages.SUCCESS)

resend_promotion_email.short_description = _('Отправить email с акцией')


@admin.register(DiscountModel)
class DiscountModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_show', 'is_active')
    actions = [resend_promotion_email]


@admin.register(LoyaltyModel)
class LoyaltyAdmin(admin.ModelAdmin):
    list_display = ('level', 'discount_percentage', 'sum_step')
