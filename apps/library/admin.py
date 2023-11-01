from django.contrib import admin

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
