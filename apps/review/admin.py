from django.contrib import admin
from apps.review.models import ReviewProductModel, ReviewImage
from django.utils.translation import gettext_lazy as _


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(ReviewProductModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'count_stars', 'date_created']
    # readonly_fields = ('count_stars', 'review_text', 'product', 'user', 'date_created' )
    search_fields = ('id', 'product', 'user')
    list_filter = ('count_stars', )
    inlines = [ReviewImageInline, ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        model_name = _(self.model._meta.verbose_name_plural)
        extra_context['model_name'] = model_name
        return super().changelist_view(request, extra_context=extra_context)

