from django.contrib import admin
from apps.review.models import ReviewProductModel, ReviewImage


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

