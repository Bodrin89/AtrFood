from django.contrib import admin
from django.utils.html import format_html

from apps.library.models import (
    City,
    CountryManufacturer,
    District,
    ManufacturingCompany,
    NameLevelLoyalty,
    PackageType,
    ReturnPolicy,
    PrivacyPolicy,
    AboutCompany,
    Region,
    AddressArtFood,
    ContactArtFood,
    OpenStore,
    SocialNetwork,

)


@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(CountryManufacturer)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ManufacturingCompany)
class ManufacturingCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(NameLevelLoyalty)
class NameLevelLoyaltyAdmin(admin.ModelAdmin):
    pass


@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    pass


class ContactArtFoodInline(admin.TabularInline):
    model = ContactArtFood
    extra = 1


class OpenStoreInline(admin.TabularInline):
    model = OpenStore
    extra = 1


@admin.register(AddressArtFood)
class AddressArtFoodAdmin(admin.ModelAdmin):
    inlines = [OpenStoreInline, ContactArtFoodInline]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    pass
